import json
import random
import time
import logging
import traceback
from paho.mqtt import client as mqtt_client
 

BROKER = 'obe60107-internet-facing-41f559212072570b.elb.us-east-1.amazonaws.com'
PORT = 1883
TOPIC = "iot-group-06"

# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-{id}".format(id=random.randint(0, 1000))
USERNAME = 'quannv'
PASSWORD = 'quannv'
FLAG_CONNECTED = 0


def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def publish(client):
    cnt = 0
    while True:
        message = {
            'Id': cnt, 
            "u": random.randint(1, 10), 
            "v": random.randint(1, 10), 
            "w": random.randint(1, 10)
        }
        message = json.dumps(message)
        result = client.publish(TOPIC, message)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send {message} to topic {TOPIC}")
        else:
            print("Failed to send message to topic {topic}".format(topic=TOPIC))
        cnt += 1
        time.sleep(1)


def run():
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if FLAG_CONNECTED:
        publish(client)
    else:
        client.loop_stop()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logging.error(traceback.format_exc())

