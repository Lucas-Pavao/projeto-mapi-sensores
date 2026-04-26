import time
import json
import random
from datetime import datetime
from collections import deque


class VirtualSensor:
    def __init__(self, collector, id_sensor, mqtt_manager=None, intervalo_segundos=300):
        self.collector = collector
        self.id_sensor = id_sensor
        self.intervalo_padrao = intervalo_segundos
        self.intervalo_atual = intervalo_segundos
        self.mqtt_manager = mqtt_manager
        self.ativo = False
        
        # Lógica de Fog: Histórico para média móvel e detecção de anomalias
        self.historico_leituras = deque(maxlen=10)
        self.limiar_anomalia = 1.5  # 50% acima da média
        self.bateria = 100.0

    def iniciar_monitoramento(self, **kwargs):
        self.ativo = True
        print(f"[*] Sensor Virtual {self.id_sensor} ATIVADO (Frequência: {self.intervalo_atual}s).")

        while self.ativo:
            try:
                # print(f"[{datetime.now().strftime('%H:%M:%S')} | {self.id_sensor}] Coletando dados...")

                dados = self.collector.buscar_dados(**kwargs)

                if dados:
                    # Se 'dados' for uma lista, processamos a leitura mais recente para a lógica de Fog
                    # mas enviamos o conjunto completo de informações no payload
                    leitura_recente = dados[0] if isinstance(dados, list) and len(dados) > 0 else dados
                    
                    valor_principal = self._extrair_valor_relevante(leitura_recente)
                    if valor_principal is not None:
                        self._aplicar_logica_fog(valor_principal)
                    
                    payload = self._gerar_payload(leitura_recente, valor_principal)
                    if self.mqtt_manager:
                        self._publicar_mqtt(payload)
                else:
                    print(f"[!] Sem dados novos para {self.id_sensor}.")

                # Simulação de consumo de bateria
                self.bateria = max(0, self.bateria - random.uniform(0.01, 0.05))
                
                time.sleep(self.intervalo_atual)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[Erro no {self.id_sensor}]: {e}")
                time.sleep(self.intervalo_padrao)

    def _extrair_valor_relevante(self, leitura):
        """Extrai um valor numérico principal para análise de anomalias."""
        try:
            # ANA
            if 'Chuva_Adotada' in leitura:
                return float(leitura.get('Chuva_Adotada', 0) or 0)
            
            # APAC Cemaden
            if 'chuva_acumulada' in leitura:
                return float(leitura.get('chuva_acumulada', 0) or 0)
            
            # APAC Meteorologia
            if 'precipitacao_acumulada' in leitura:
                return float(leitura.get('precipitacao_acumulada', 0) or 0)
        except:
            pass
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
        """Gera o JSON contendo todas as informações da API + metadados de Fog."""
        payload = {
            "id_sensor": self.id_sensor,
            "timestamp_coleta": datetime.now().isoformat(),
            "status_bateria": f"{self.bateria:.1f}%",
            "fog_valor_referencia": valor_principal,
            "dados_originais": leitura_completa
        }
        return payload

    def _publicar_mqtt(self, payload):
        topic = f"projeto-mapi/sensores/{self.id_sensor}"
        self.mqtt_manager.publish(topic, payload)
        print(f"[MQTT] Payload enviado para {self.id_sensor} (Dados completos incluídos).")

    def parar(self):
        self.ativo = False
        print(f"[!] Sensor {self.id_sensor} DESATIVADO.")