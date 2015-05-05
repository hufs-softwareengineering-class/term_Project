import Adafuit_BBIO.ADC as ADC

def GPIOlightRead():
  ADC.setup() 
  return ADC.read("P9_33")

