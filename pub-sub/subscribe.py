import random
from elasticsearch import Elasticsearch
from paho.mqtt import client as mqtt_client
import json
import traceback
import logging
from datetime import datetime

broker = 'obe60107-internet-facing-41f559212072570b.elb.us-east-1.amazonaws.com'
port = 1883
topic = "iot-group-06"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'quannv'
password = 'quannv'

elastic = Elasticsearch()

def send_data(document, index="iot-data"):
  key = str(document["time"])
  elastic.index(index=index, id=key, document=document)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")
 
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, message):
        document = str(message.payload.decode("utf-8")).replace("\'", "\"")
        if document != "Conection from ESP8266 established":
            document = json.loads(document)
            document["time"] = datetime.now().strftime("%H:%M:%S %m-%d-%Y")
            send_data(document)
        print(document)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logging.error(traceback.format_exc())

