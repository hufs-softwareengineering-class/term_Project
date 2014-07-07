import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_12", GPIO.OUT)

def function(inputdata):
  if inputdata == 1:
    GPIO.output("P8_12", GPIO.HIGH)
  else:
    GPIO.output("P8_12", GPIO.LOW)







