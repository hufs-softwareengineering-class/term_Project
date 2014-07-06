import Adafruit_BBIO.ADC as ADC

def GPIOtemperRead():
  ADC.setup()
  return ADC.read("  ") #fill the blank port num and pinnum
