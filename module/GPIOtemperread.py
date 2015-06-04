import Adafruit_BBIO.ADC as ADC

def GPIOtemperRead():
  ADC.setup()
  return ( ADC.read("p8_14") - 500 )/10 #fill the blank port num and pinnum
