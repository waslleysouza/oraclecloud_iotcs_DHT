#!/usr/bin/python3
# Waslley Souza (waslleys@gmail.com)
# 2018

import Adafruit_DHT
import time
import json
import os
import platform
from oraclecloud import Iot


USER = 'iot'
PASS = 'welcome1'
URL  = 'https://iotcs.oraclecloud.com:10443'
SHARED_SECRET = 'Welcome_1'

DEVICE_MODEL_URN = "urn:com:oracle:iot:device:temp_hum"
DEVICE_MODEL_FORMAT_URN = DEVICE_MODEL_URN + ":message"


sensor = Adafruit_DHT.DHT11
#sensor = Adafruit_DHT.DHT22

# GPIO pin
pino_sensor = 14


def main():
    print('Running...')
    
    while True:
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pino_sensor)

      if humidity is not None and temperature is not None:
        print("Temperature = {0:0.1f} C  Humidity = {1:0.1f} %".format(temperature, humidity))
        data = {'humidity':humidity,'temperature':temperature}
        iot.send_message(device, DEVICE_MODEL_FORMAT_URN, data)
        time.sleep(1)
      
      else:
        print("Error !!!")


def _open_file(file_name):
    f = open(file_name, 'r')
    text = f.read()
    f.close()
    return text


def _create_file(file_name, text):
    f = open(file_name, 'w')
    f.write(text)
    f.close()


if __name__ == "__main__":
    iot = Iot(USER, PASS, URL, False)

    if os.path.isfile('device.txt'):
        device_id = _open_file('device.txt')
        device = iot.get_device(device_id)  
        iot.set_shared_secret(SHARED_SECRET)

    else:
        device_model = iot.get_device_model(DEVICE_MODEL_URN)
        if not device_model:
            formats = json.loads(_open_file('formats.json'))
            device_model = iot.create_device_model("TemperatureHumidity", DEVICE_MODEL_URN, formats)

        device_name = platform.node() + "_TempHum"
        device = iot.create_device(device_name, SHARED_SECRET, hardware_id=device_name)
        iot.activate_device(device, device_model["urn"])

        _create_file('device.txt', device['id'])
    
    main()