import time
from machine import Pin

led = Pin(2, Pin.OUT) # There are two LEDs 2, 16

# while True:
#     if led.value() == 0:
#         led.value(1)
#     else:
#         led.value(0)
#     time.sleep(1)
    
from machine import Timer
tim = Timer(-1)

def timer_fn(t):
    if led.value() == 0:
        led.value(1)
    else:
        led.value(0)

tim.init(period=1000, mode=Timer.PERIODIC, callback=timer_fn)