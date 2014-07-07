import Adafruit_DHT
import time

def GPIOhumidRead():
  sensor =  Adafruit_DHT.DHT11
  pin = "P9_11"

  humid, temp = Adafruit_DHT.read_retry(sensor, pin)

  return humid
