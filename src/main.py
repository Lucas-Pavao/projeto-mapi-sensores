import threading
import time
import sys
import os
from src.services.auth_manager import AuthManager
from src.services.mqtt_manager import MQTTManager
from src.collectors.ana_rest_collector import AnaRestCollector
from src.collectors.apac_meteorologia24h_collector import ApacCollectorMeteorologia24h
from src.collectors.apac_cemaden_collector import ApacCemadenCollector
from src.controllers.sensor_manager import VirtualSensor

def main():
    print("\n" + "="*50)
    print("      INICIALIZANDO MALHA IOT - PROJETO MAPI")
    print("      (Modo Automático: Malha Completa Ativa)")
    print("="*50)

    # ==========================================
    # 1. SETUP DE SERVIÇOS (Auth e MQTT)
    # ==========================================
    auth = AuthManager()
    # Configurações via .env
    mqtt = MQTTManager() 
    mqtt.connect()

    sensores_ativos = []
    threads = []
    
    # ==========================================
    # 2. DEPLOY DOS COLETORES (MALHA COMPLETA)
    # ==========================================
    
    # --- APAC (Agência Pernambucana de Águas e Clima) ---
    coletor_meteorologia = ApacCollectorMeteorologia24h()
    coletor_cemaden = ApacCemadenCollector()

    print("\n[VIRTUALIZATION] Provisionando sensores APAC via Scraping JSON...")
    print("  -> Fontes: Meteorologia 24h e Pluviômetros Cemaden")
    
    rmr_cidades = [
        "RECIFE", "OLINDA", "JABOATAO DOS GUARARAPES", "PAULISTA", 
        "CAMARAGIBE", "CABO DE SANTO AGOSTINHO", "SAO LOURENCO DA MATA", 
        "MORENO", "IGARASSU", "IPOJUCA"
    ]

    def deploy_sensores_apac(coletor, prefixo_id):
        # Busca todas as estações disponíveis
        todas_estacoes = coletor.buscar_dados()
        if not todas_estacoes:
            return

        from src.utils.text_utils import remover_acentos
        
        estacoes_rmr = []
        for e in todas_estacoes:
            muni = remover_acentos(e.get('municipio', '').upper())
            nome = remover_acentos(e.get('estacao_nome', '').upper())
            
            # Filtro por cidade
            na_rmr = any(remover_acentos(c) in muni or remover_acentos(c) in nome for c in rmr_cidades)
            
            # Casos especiais: Estações que sabemos ser da RMR mas estão sem cidade no JSON
            termos_especiais = ["SEDE", "CASTELO BRANCO", "COMPESA", "IMBIRIBEIRA", "NOVA DESCOBERTA", "ALDEIA"]
            if muni == "NAO INFORMADA" or muni == "":
                if any(t in nome for t in termos_especiais):
                    na_rmr = True

            if na_rmr:
                estacoes_rmr.append(e)

        # Remove duplicatas (mesmo nome na mesma cidade)
        vistas = set()
        for e in estacoes_rmr:
            key = (e['estacao_nome'], e['municipio'])
            if key in vistas:
                continue
            vistas.add(key)

            # Criar ID amigável: PREFIXO-CIDADE-ESTACAO
            cidade_id = remover_acentos(e['municipio'].split()[0].upper()) if e['municipio'] != "Não informada" else "RMR"
            
            # Limpa o nome da estação para o ID
            nome_limpo = e['estacao_nome'].replace("[APAC]", "").replace("[CEMADEN]", "").replace("[", "").replace("]", "").strip()
            nome_id = remover_acentos(nome_limpo.split()[0].upper())
            id_sensor = f"{prefixo_id}-{cidade_id}-{nome_id}"

            s = VirtualSensor(coletor, id_sensor, mqtt_manager=mqtt, intervalo_segundos=60)
            sensores_ativos.append(s)
            t = threading.Thread(
                target=s.iniciar_monitoramento, 
                kwargs={'filtro_estacao': e['estacao_nome']}, 
                daemon=True
            )
            t.start()
            threads.append(t)
            # print(f"  [+] Sensor {id_sensor} provisionado para {e['estacao_nome']} ({e['municipio']})")

    deploy_sensores_apac(coletor_meteorologia, "APAC-METEO")
    deploy_sensores_apac(coletor_cemaden, "APAC-PLUVIO")

    # --- ANA (Agência Nacional de Águas) ---
    coletor_ana = AnaRestCollector(auth)
    # Estações: Rio Capibaribe (São Lourenço) e Barreiros
    estacoes_ana = ["39187800", "39590000"] 
    data_hoje = time.strftime("%Y-%m-%d")

    print("\n[VIRTUALIZATION] Provisionando sensores ANA via API REST...")
    print("  -> Fonte: Rede Hidrometeorológica Nacional (Telemetria)")
    
    for cod in estacoes_ana:
        nome_rio = "CAPIBARIBE" if cod == "39187800" else "BARREIROS"
        id_a = f"ANA-TELE-{nome_rio}"
        s_a = VirtualSensor(coletor_ana, id_a, mqtt_manager=mqtt, intervalo_segundos=120)
        sensores_ativos.append(s_a)
        t_a = threading.Thread(target=s_a.iniciar_monitoramento, kwargs={
            'cod_estacao': cod, 
            'data_busca': data_hoje
        }, daemon=True)
        t_a.start()
        threads.append(t_a)

    # ==========================================
    # 3. MONITORAMENTO DO SISTEMA
    # ==========================================
    topic_prefix = os.getenv("MQTT_TOPIC_PREFIX", "projeto-mapi/sensores")
    print(f"\n[SISTEMA] {len(sensores_ativos)} sensores virtuais em execução paralela.")
    print(f"[SISTEMA] Broker MQTT: {os.getenv('MQTT_BROKER', 'broker.hivemq.com')}")
    print(f"[SISTEMA] Tópico base: {topic_prefix}/#")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Encerrando malha de sensores...")
        for sensor in sensores_ativos:
            sensor.parar()
        mqtt.disconnect()

if __name__ == "__main__":
    main()