import threading
import time
from src.services.auth_manager import AuthManager
from src.collectors.ana_rest_collector import AnaRestCollector
from src.collectors.apac_meteorologia24h_collector import ApacCollectorMeteorologia24h
from src.collectors.apac_cemaden_collector import ApacCemadenCollector
from src.controllers.sensor_manager import VirtualSensor

def main():
    # ==========================================
    # 1. SETUP DE COLETORES (Drivers dos Sensores)
    # ==========================================
    auth = AuthManager()
    coletor_ana = AnaRestCollector(auth)
    coletor_meteorologia = ApacCollectorMeteorologia24h()
    coletor_cemaden = ApacCemadenCollector()

    cidades_alvo = [
        "RECIFE", "OLINDA", "JABOATÃO DOS GUARARAPES",
        "PAULISTA", "CABO DE SANTO AGOSTINHO", "IPOJUCA", "IGARASSU"
    ]

    sensores_ativos = []
    threads = []

    print("Iniciando provisionamento da malha IoT...\n")

    # ==========================================
    # 2. DEPLOY DA MALHA DE SENSORES CLIMÁTICOS (Meteorologia 24h)
    # ==========================================
    print("-> Subindo rede de Estações Climáticas...")
    for cidade in cidades_alvo:
        # ID Único para o sensor de clima
        id_sensor = f"CLIMA-{cidade}"
        sensor = VirtualSensor(coletor_meteorologia, id_sensor, intervalo_segundos=600)
        sensores_ativos.append(sensor)

        t = threading.Thread(target=sensor.iniciar_monitoramento, kwargs={'filtro_cidade': cidade})
        t.daemon = True
        t.start()
        threads.append(t)

    # Pequeno delay apenas para não embolar os prints no terminal
    time.sleep(2)

    # ==========================================
    # 3. DEPLOY DA MALHA DE PLUVIÔMETROS (Cemaden)
    # ==========================================
    print("\n-> Subindo rede de Pluviômetros e Sensores Geotécnicos...")
    for cidade in cidades_alvo:
        # ID Único para o sensor de chuva/solo
        id_sensor = f"PLUVIO-{cidade}"
        sensor = VirtualSensor(coletor_cemaden, id_sensor, intervalo_segundos=600)
        sensores_ativos.append(sensor)

        t = threading.Thread(target=sensor.iniciar_monitoramento, kwargs={'filtro_cidade': cidade})
        t.daemon = True
        t.start()
        threads.append(t)

    # ==========================================
    # 4. LOOP PRINCIPAL (Mantém o sistema vivo)
    # ==========================================
    print("\n[+] Todas as threads de sensores foram iniciadas. Aguardando leituras...\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Sinal de interrupção recebido. Desativando todos os nós...")
        for sensor in sensores_ativos:
            sensor.parar()

if __name__ == "__main__":
    main()