import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_12", GPIO.OUT)

while True:
    GPIO.output("P8_12", GPIO.HIGH)
    time.sleep(1)
    GPIO.output("P8_12", GPIO.LOW)
    time.sleep(1)

