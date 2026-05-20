import os
import time
from unittest.mock import MagicMock
from src.controllers.sensor_manager import VirtualSensor

def test_battery_cycle():
    print("--- Iniciando Teste de Ciclo de Bateria ---")
    
    # Mock do coletor e mqtt
    mock_collector = MagicMock()
    mock_collector.buscar_dados.return_value = {"Chuva_Adotada": 10.5, "estacao_nome": "Teste"}
    mock_mqtt = MagicMock()

    # Configurações aceleradas para o teste
    os.environ["SENSOR_BATTERY_DRAIN_RATE"] = "40.0" # 40% por ciclo
    os.environ["SENSOR_BATTERY_CHARGE_RATE"] = "50.0" # 50% por ciclo
    os.environ["SENSOR_DEFAULT_INTERVAL"] = "1"

    sensor = VirtualSensor(mock_collector, "TEST-SENSOR", mqtt_manager=mock_mqtt, intervalo_segundos=1)
    
    # Ciclo 1: Ativo (100% -> 60%)
    print(f"Bateria Inicial: {sensor.bateria}% | Estado: {sensor.estado}")
    sensor._ciclo_ativo()
    print(f"Bateria após Ciclo 1: {sensor.bateria:.1f}% | Estado: {sensor.estado}")
    assert sensor.estado == "ATIVO"
    
    # Ciclo 2: Ativo (60% -> 20%)
    sensor._ciclo_ativo()
    print(f"Bateria após Ciclo 2: {sensor.bateria:.1f}% | Estado: {sensor.estado}")
    
    # Ciclo 3: Esgotamento (20% -> 0% -> CARREGANDO)
    sensor._ciclo_ativo()
    print(f"Bateria após Ciclo 3: {sensor.bateria:.1f}% | Estado: {sensor.estado}")
    assert sensor.estado == "CARREGANDO"
    
    # Ciclo 4: Carregando (0% -> 50%)
    sensor._ciclo_carregamento()
    print(f"Bateria após Ciclo 4 (Carga): {sensor.bateria:.1f}% | Estado: {sensor.estado}")
    assert sensor.estado == "CARREGANDO"
    
    # Ciclo 5: Carregando (50% -> 100% -> ATIVO)
    sensor._ciclo_carregamento()
    print(f"Bateria após Ciclo 5 (Carga): {sensor.bateria:.1f}% | Estado: {sensor.estado}")
    assert sensor.estado == "ATIVO"

    print("--- Teste de Ciclo de Bateria Concluído com Sucesso! ---")

if __name__ == "__main__":
    test_battery_cycle()
