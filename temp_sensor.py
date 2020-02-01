#!/usr/bin/env python3
import Adafruit_DHT

class SensorError(Exception):
  pass

def measure():
  sensor = Adafruit_DHT.DHT22
  pin = 4

  for i in range(3):
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity and temperature:
      return humidity, temperature
    continue
  raise SensorError
