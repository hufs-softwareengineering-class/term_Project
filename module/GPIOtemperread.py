import Adafuit_BBIO.ADC as ADC

def GPIOlightRead():
  ADC.setup()
  return ADC.read("  ") #fill the blank port num and pinnum
