import Adafruit_BBIO.ADC as ADC

def GPIOlightRead():
  ADC.setup() 
  value =  ADC.read("P9_33")
  if value >= 0.3: # state of turn on the romm's light
    return 1
  else:
    return 0


