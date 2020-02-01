#!/usr/bin/env python3
import temp_sensor
import yaml
import json
import time
import sys
import signal
from kafka import KafkaProducer

def terminate(signalNumber, frame):
    print ('(SIGTERM) terminating the process')
    sys.exit()

def send(topic):

  resources_path = sys.path[0] + "/resources/"
  with open(resources_path + "config.yaml",'r') as f:
      config = yaml.safe_load(f)

  producer = KafkaProducer(
      bootstrap_servers=config['kafka']['bootstrap_servers'],
      security_protocol='SSL',
      ssl_cafile=resources_path+config['kafka']['ssl_cafile'],
      ssl_keyfile=resources_path+config['kafka']['ssl_keyfile'],
      ssl_certfile=resources_path+config['kafka']['ssl_certfile']
      )

  humidity, temperature = temp_sensor.measure()
  timestamp = time.strftime("%y%m%d%H%M",time.localtime())

  message = {
      "timestamp": timestamp,
      "temperature": temperature,
      "humidity": humidity
      }

  producer.send(topic, json.dumps(message).encode('utf-8'))
  # Need to flush, as the message is not sent instantly and if the scripts finishes before, the message is not sent at all anymore
  producer.flush()
  print("Topic: {}; Measurement: {}".format(topic, json.dumps(message)))

if __name__ == "__main__":
  signal.signal(signal.SIGTERM, terminate)
  signal.signal(signal.SIGINT, terminate)
  while True:
    send('temperature')
    time.sleep(1800)
