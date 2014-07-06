import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P8_7", GPIO.IN)
def GPIOmagnetRead():
if GPIO.input("P8_7") == True:
        print "Door is close..."
	return 0
else:
        print "Door is OPEN!"
	return 1
