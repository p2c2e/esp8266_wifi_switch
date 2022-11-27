import time
from machine import Pin

led = Pin(2, Pin.OUT) # There are two LEDs 2, 16

myled = Pin(12, Pin.OUT) # GPIO5 - 29th out of 30 pins
myled.value(0)

while True:
    if led.value() == 0:
        led.value(1)
    else:
        led.value(0)
    time.sleep(1)