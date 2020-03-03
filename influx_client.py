#!/usr/bin/env python3

import temp_sensor
import json
import time
import sys
import yaml
import signal
from influxdb import InfluxDBClient
from influxdb import exceptions as inf
from requests import exceptions as req

resources_path = sys.path[0] + "/resources/"
with open(resources_path + "config.yaml", "r") as f:
    config = yaml.safe_load(f)

def terminate(signalNumber, frame):
    print ('(SIGTERM) terminating the process')
    sys.exit()

def insert(client):
  try:
    humidity, temperature = temp_sensor.measure()
    timestamp = time.ctime()
    data = [
    {
        "measurement": config["measurement"],
        "time": timestamp,
        "fields": {
          "humidity": humidity,
          "temperature": temperature
        }
     }
    ]
    client.write_points(data)
    print("Successfully inserted {}".format(json.dumps(data)))
  except temp_sensor.SensorError:
    pass

def connect():
  client = InfluxDBClient(host=config["db_host"], port=config["db_port"], 
          username=config["db_username"], password=config["db_password"], 
          database=config["db_name"], ssl=True, verify_ssl=True)
  return client

if __name__ == "__main__":
  signal.signal(signal.SIGTERM, terminate)
  signal.signal(signal.SIGINT, terminate)
  client = connect()
  while True:
    try:
      insert(client)
    except (req.ConnectionError,inf.InfluxDBServerError) as e:
      print("Failed insert")
      client.close()
      connect()
      insert(client)
    finally:
      time.sleep(60)
