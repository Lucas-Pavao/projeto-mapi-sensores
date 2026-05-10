import os
import paho.mqtt.client as mqtt
import json
import logging
from dotenv import load_dotenv

load_dotenv()

class MQTTManager:
    def __init__(self, broker=None, port=None, client_id=None, keepalive=60):
        self.broker = broker or os.getenv("MQTT_BROKER", "broker.hivemq.com")
        self.port = int(port or os.getenv("MQTT_PORT", 1883))
        self.client_id = client_id
        self.keepalive = keepalive
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Conectado ao broker {self.broker}")
        else:
            print(f"[MQTT] Falha na conexão, código de retorno: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        print(f"[MQTT] Desconectado do broker {self.broker}")

    def _on_publish(self, client, userdata, mid):
        # logging.debug(f"[MQTT] Mensagem {mid} publicada com sucesso.")
        pass

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            self.client.loop_start()
        except Exception as e:
            print(f"[MQTT] Erro ao conectar: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message, qos=0, retain=False):
        if isinstance(message, (dict, list)):
            message = json.dumps(message)
        
        result = self.client.publish(topic, message, qos=qos, retain=retain)
        status = result[0]
        if status != 0:
            print(f"[MQTT] Falha ao enviar mensagem para o tópico {topic}")
