import Adafruit_BBIO.GPIO as GPIO
import time

def GPIOtemperWriter(num):
  GPIO.setup("P8_14", GPIO.OUT) # air condinational
  GPIO.setup("P8_16", GPIO.OUT) # heater


  if num == 0:
    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_16", GPIO.HIGH)
  elif num == 1:
    GPIO.output("P8_14", GPIO.HIGH)
    GPIO.output("P8_16", GPIO.LOW)
  else: # num == -1
    GPIO.output("P8_14", GPIO.LOW)
    GPIO.output("P8_16", GPIO.LOW)

