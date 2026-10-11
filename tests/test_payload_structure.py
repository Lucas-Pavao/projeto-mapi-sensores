import os
import json
from unittest.mock import MagicMock
from src.controllers.sensor_manager import VirtualSensor

def test_payload_flattening():
    print("--- Iniciando Teste de Achatamento de Payload ---")
    
    # Mock do coletor e mqtt
    mock_collector = MagicMock()
    # Simula retorno de dados da APAC ou ANA (já no formato de lista de itens após minha correção)
    mock_collector.buscar_dados.return_value = [{
        "chuva_acumulada": 15.0,
        "estacao_nome": "Estacao Teste",
        "municipio": "Cidade Teste",
        "codigo": "123"
    }]
    
    mock_mqtt = MagicMock()

    sensor = VirtualSensor(mock_collector, "TEST-PAYLOAD", mqtt_manager=mock_mqtt)
    
    # Executa um ciclo ativo
    sensor._ciclo_ativo()
    
    # Verifica a chamada do MQTT
    args, kwargs = mock_mqtt.publish.call_args
    topic = args[0]
    payload = args[1]
    
    print(f"Tópico: {topic}")
    print(f"Payload publicado: {json.dumps(payload, indent=2)}")
    
    # Asserções
    assert "id_sensor" in payload
    assert payload["id_sensor"] == "TEST-PAYLOAD"
    assert "status_bateria" in payload
    assert "fog_valor_referencia" in payload
    assert payload["fog_valor_referencia"] == 15.0
    
    # Verifica se os campos internos foram promovidos ao topo
    assert "chuva_acumulada" in payload
    assert payload["chuva_acumulada"] == 15.0
    assert "estacao_nome" in payload
    assert payload["estacao_nome"] == "Estacao Teste"
    
    # Verifica que o campo 'dados_originais' NÃO existe mais
    assert "dados_originais" not in payload
    
    print("--- Teste de Achatamento de Payload Concluído com Sucesso! ---")

if __name__ == "__main__":
    test_payload_flattening()
