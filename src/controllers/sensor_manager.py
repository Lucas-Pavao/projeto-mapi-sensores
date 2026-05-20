import os
import time
import json
import random
from datetime import datetime
from collections import deque


class VirtualSensor:
    def __init__(self, collector, id_sensor, mqtt_manager=None, intervalo_segundos=300):
        self.collector = collector
        self.id_sensor = id_sensor
        self.intervalo_padrao = int(os.getenv("SENSOR_DEFAULT_INTERVAL", intervalo_segundos))
        self.intervalo_atual = self.intervalo_padrao
        self.mqtt_manager = mqtt_manager
        self.ativo = False
        self.estado = "ATIVO"  # Estados possíveis: ATIVO, CARREGANDO
        
        # Lógica de Fog: Histórico para média móvel e detecção de anomalias
        self.historico_leituras = deque(maxlen=int(os.getenv("SENSOR_HISTORY_SIZE", 10)))
        self.limiar_anomalia = float(os.getenv("SENSOR_ANOMALY_THRESHOLD", 1.5))
        
        # Configurações de Bateria
        self.bateria = 100.0
        self.taxa_dreno_base = float(os.getenv("SENSOR_BATTERY_DRAIN_RATE", 0.05))
        self.taxa_recarga = float(os.getenv("SENSOR_BATTERY_CHARGE_RATE", 1.0))

    def iniciar_monitoramento(self, **kwargs):
        self.ativo = True
        print(f"[*] Sensor Virtual {self.id_sensor} ATIVADO (Frequência: {self.intervalo_atual}s).")

        while self.ativo:
            try:
                if self.estado == "ATIVO":
                    self._ciclo_ativo(**kwargs)
                else:
                    self._ciclo_carregamento()

                time.sleep(self.intervalo_atual)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[Erro no {self.id_sensor}]: {e}")
                time.sleep(self.intervalo_padrao)

    def _ciclo_ativo(self, **kwargs):
        """Lógica executada quando o sensor tem bateria."""
        dados = self.collector.buscar_dados(**kwargs)

        valor_principal = None
        leitura_recente = None

        if dados:
            leitura_recente = dados[0] if isinstance(dados, list) and len(dados) > 0 else dados
            valor_principal = self._extrair_valor_relevante(leitura_recente)
            if valor_principal is not None:
                self._aplicar_logica_fog(valor_principal)
        
        # Gera e publica payload
        payload = self._gerar_payload(leitura_recente, valor_principal)
        if self.mqtt_manager:
            self._publicar_mqtt(payload)

        # Consumo de bateria
        fator_dreno = 1.0 if self.intervalo_atual == self.intervalo_padrao else 3.0
        dreno = (random.uniform(self.taxa_dreno_base * 0.8, self.taxa_dreno_base * 1.2)) * fator_dreno
        self.bateria = max(0, self.bateria - dreno)

        if self.bateria <= 0:
            self.estado = "CARREGANDO"
            print(f"[BATTERY ALERT] Sensor {self.id_sensor} descarregado. Entrando em modo de CARREGAMENTO.")

    def _ciclo_carregamento(self):
        """Lógica executada quando o sensor está sem bateria."""
        # Recarga
        self.bateria = min(100.0, self.bateria + self.taxa_recarga)
        
        # Payload reduzido
        payload = {
            "id_sensor": self.id_sensor,
            "timestamp_coleta": datetime.now().isoformat(),
            "estado": self.estado,
            "status_bateria": f"{self.bateria:.1f}%",
            "mensagem": "Sensor em modo de recarga solar. Coleta suspensa."
        }
        
        if self.mqtt_manager:
            self._publicar_mqtt(payload)

        if self.bateria >= 100.0:
            self.estado = "ATIVO"
            print(f"[BATTERY INFO] Sensor {self.id_sensor} totalmente carregado. Retornando às operações.")

    def _extrair_valor_relevante(self, leitura):
        """Extrai um valor numérico principal para análise de anomalias."""
        # Chaves prioritárias para diferentes fontes (Expandido para abranger mais tipos da ANA)
        chaves_prioritarias = [
            'chuva_acumulada', 'precipitacao_acumulada', 'Chuva_Adotada', 'chuva',
            'Nivel_Adotado', 'nivel', 
            'Vazao_Adotada', 'vazao',
            'Temperatura_Adotada', 'temperatura_ar',
            'Turbidez_Adotada', 'turbidez',
            'Ph_Adotado', 'ph',
            'Umidade_Adotada', 'umidade_relativa'
        ]

        for chave in chaves_prioritarias:
            if chave in leitura:
                val = leitura.get(chave)
                try:
                    return float(val) if val is not None else 0.0
                except (ValueError, TypeError):
                    continue
        return None

    def _aplicar_logica_fog(self, valor):
        """Processamento local: Média móvel e Frequência Adaptativa."""
        if len(self.historico_leituras) > 0:
            media = sum(self.historico_leituras) / len(self.historico_leituras)
            
            # Detecção de Anomalia: Se o valor subir bruscamente
            if valor > (media * self.limiar_anomalia) and valor > 0.5:
                if self.intervalo_atual == self.intervalo_padrao:
                    print(f"[FOG ALERT] Anomalia detectada em {self.id_sensor} ({valor} > {media:.2f}). Aumentando frequência!")
                    self.intervalo_atual = max(30, self.intervalo_padrao // 5)
            else:
                if self.intervalo_atual != self.intervalo_padrao:
                    print(f"[FOG INFO] Níveis normalizados em {self.id_sensor}. Restaurando frequência padrão.")
                    self.intervalo_atual = self.intervalo_padrao
        
        self.historico_leituras.append(valor)

    def _gerar_payload(self, leitura_completa, valor_principal):
        """Gera o JSON contendo todas as informações da API + metadados de Fog de forma achatada."""
        payload = {
            "id_sensor": self.id_sensor,
            "timestamp_coleta": datetime.now().isoformat(),
            "status_bateria": f"{self.bateria:.1f}%",
            "fog_valor_referencia": valor_principal
        }

        if isinstance(leitura_completa, dict):
            payload.update(leitura_completa)

        return payload

    def _publicar_mqtt(self, payload):
        prefix = os.getenv("MQTT_TOPIC_PREFIX", "projeto-mapi/sensores")
        topic = f"{prefix}/{self.id_sensor}"
        self.mqtt_manager.publish(topic, payload)
        
        # Log mais específico sobre a origem
        origem = "Agência Nacional de Águas (ANA)" if "ANA" in self.id_sensor else "APAC - Pernambuco"
        print(f"[MQTT | {self.id_sensor}] Dados enviados. Fonte: {origem}.")

    def parar(self):
        self.ativo = False
        print(f"[!] Sensor {self.id_sensor} DESATIVADO.")