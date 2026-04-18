import time
from datetime import datetime


class VirtualSensor:
    def __init__(self, collector, cod_estacao, intervalo_segundos=300):
        self.collector = collector
        self.cod_estacao = cod_estacao
        self.intervalo = intervalo_segundos
        self.ativo = False

    def iniciar_monitoramento(self, **kwargs):
        self.ativo = True
        print(f"[*] Sensor Virtual {self.cod_estacao} ATIVADO.")

        while self.ativo:
            try:
                print(f"[{datetime.now().strftime('%H:%M:%S')} | {self.cod_estacao}] Coletando dados...")

                dados = self.collector.buscar_dados(**kwargs)

                if dados:
                    self._processar_dados(dados)
                else:
                    print(f"[!] Sem dados novos para {self.cod_estacao}.")

                time.sleep(self.intervalo)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[Erro no {self.cod_estacao}]: {e}")
                time.sleep(self.intervalo)

    def _processar_dados(self, dados):
        if isinstance(dados, list) and len(dados) > 0:
            print(f"\n=== LEITURA: {self.cod_estacao} ({len(dados)} estações operantes) ===")

            for leitura in dados:
                if 'municipio' in leitura and 'fonte' in leitura and 'APAC' in leitura['fonte']:
                    nome = leitura.get('estacao_nome', 'Desconhecida')
                    tipo = leitura.get('tipo', 'N/A')

                    print(f" -> Estação: {nome} ({tipo})")
                    print(f"    Coordenadas: Lat {leitura.get('latitude')} | Lon {leitura.get('longitude')}")

                    temp = leitura.get('temperatura_ar')
                    umid_ar = leitura.get('umidade_relativa')
                    if temp is not None:
                        print(f"    Clima: {temp}°C | Umidade do Ar: {umid_ar}%")

                    rad = leitura.get('radiacao_solar')
                    if rad is not None:
                        print(f"    Radiação Solar: {rad}")

                    print(f"    Precipitação Acumulada: {leitura.get('precipitacao_acumulada')} mm")

                    umidade_solo = leitura.get('umidade_solo')
                    if umidade_solo and any(u is not None for u in umidade_solo):
                        print(f"    Umidade do Solo (Níveis 1 a 4): {umidade_solo}")

                    print(f"    Última leitura: {leitura.get('data_hora')}")
                    print(f"    ---")

                # Lógica para ANA
                elif 'Data_Hora_Medicao' in leitura:
                    print(f"Data: {leitura.get('Data_Hora_Medicao')}")
                    print(f"Chuva: {leitura.get('Chuva_Adotada')} mm")
                    print(f"Vazão: {leitura.get('Vazao_Adotada')} m³/s")
                    print(f"    ---")

            print("=" * 50)

    def parar(self):
        self.ativo = False
        print(f"[!] Sensor {self.cod_estacao} DESATIVADO.")