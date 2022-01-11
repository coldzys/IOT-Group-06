from confluent_kafka import Producer
import socket
import json
import os

DATA_DIR = "./data"

CONF = {
  'bootstrap.servers': "172.18.0.11:29092",
  'client.id': socket.gethostname()
}

producer = Producer(CONF)

while True:
  files = os.listdir(DATA_DIR)
  if len(files) != 0:
    for file in files:
      with open(f"{DATA_DIR}/{file}") as f:
        js = json.load(f)
        producer.produce("iotTopic", key=str(js["Id"]), value=json.dumps(js))
      os.remove(f"{DATA_DIR}/{file}")
    producer.flush()

