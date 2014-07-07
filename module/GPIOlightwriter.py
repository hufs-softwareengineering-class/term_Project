import Adafruit_BBIO.GPIO as GPIO
import time

def GPIOlightWriter(num):
  GPIO.setup("P8_12", GPIO.OUT)

  if num == 1:
    GPIO.output("P8_12", GPIO.HIGH)
  else:
    GPIO.output("P8_12", GPIO.LOW)



