import Adafuit_BBIO.ADC as ADC

def GPIOhumidRead():
  ADC.setup() 
  return ADC.read("P9_33")

