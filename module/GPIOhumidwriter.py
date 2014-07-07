import Adafruit_BBIO.GPIO as GPIO
import time

def GPIOhumidWriter(num):
  GPIO.setup("P8_18", GPIO.OUT)

  if num == 1: # open window
    GPIO.output("P8_18", GPIO.HIGH)
  else: # close window
    GPIO.output("P8_18", GPIO.LOW)
