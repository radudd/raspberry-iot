#!/usr/local/bin/python
from flask import Flask, jsonify
import temp_sensor
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route("/temperature", methods = ['GET'])
def get_temperature():
    try: 
      _, temperature = temp_sensor.measure()
    except temp_sensor.SensorError:
      return jsonify({"Message": "Sensor measurement error"})
    return jsonify(
	{"Temperature": round(temperature,2),
         "Time": time.strftime("%d.%m.%Y %H:%M")
	}
    )

@app.route("/humidity", methods = ['GET'])
def get_humidity():
    try: 
      humidity, _ = temp_sensor.measure()
    except temp_sensor.SensorError:
      return jsonify({"Message": "Sensor measurement error"})
    return jsonify(
      {"Humidity": round(humidity,2),
       "Time": time.strftime("%d.%m.%Y %H:%M")
      }
    )

if __name__ == '__main__':
    app.run(debug=True)

