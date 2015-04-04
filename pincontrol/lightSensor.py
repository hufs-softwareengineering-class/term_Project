import Adafuit_BBIO.ADC as ADC
import time

ADC.setup()

whild True:
    print ADC.read("P9_33")
    time.sleep(.5)


