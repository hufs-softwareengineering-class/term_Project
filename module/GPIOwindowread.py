import Adafuit_BBIO.ADC as ADC

def GPIOwindowRead():
  ADC.setup() 
  return ADC.read("P9_33")

