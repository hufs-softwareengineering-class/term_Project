
import Adafruit_BBIO.ADC as ADC
import random
def GPIOmagnetRead():
  ADC.setup() 
  return 1#random.randint(0,1)
  #return ADC.read("P9_33")


