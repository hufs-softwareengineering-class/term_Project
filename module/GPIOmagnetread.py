
import Adafuit_BBIO.ADC as ADC

def GPIOmagnetRead():
  ADC.setup() 
  return ADC.read("P9_33")

