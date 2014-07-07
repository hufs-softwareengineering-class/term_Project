import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_7", GPIO.IN)
def GPIOmagnetRead():
	time.sleep(5)
        print "magnet read ==================="
	if GPIO.input("P8_7") == True:
		print "Close state !!!!!!!!!!!!!"
		return 0
	else:
		print "OPEN STATE !!!!!!!!!!!"
		return 1
