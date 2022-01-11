from confluent_kafka import Consumer
import json
from elasticsearch import Elasticsearch

CONF = {
  "bootstrap.servers": "172.18.0.11:29092",
  "group.id": "iotGroup",
  "auto.offset.reset": "latest"
}

consumer = Consumer(CONF)

running = True

def sendData(documents, index="iotIndex"):
  for document in documents:
    key = document["Id"]
    elastic.index(index=index, id=key, document=document)

def basic_consume_loop(consumer, topics):
  try:
    consumer.subscribe(topics)
    while running:
      msg = consumer.poll(timeout=1.0)
      if msg is None: continue
      if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
          sys.stderr.write(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n")
        elif msg.error():
          raise KafkaException(msg.error())
      else:
        documents = json.loads(msg.value())
        sendData(documents)
  finally:
    consumer.close()

def shutdown():
  running = False
    
if __name__ == "__main__":
  basic_consume_loop(consumer, ["iotTopic"])

