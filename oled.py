
from machine import I2C, Pin
import ssd1306
import time
import sh1106 

print("Before I2C")

i2c = I2C(sda=Pin(4), scl=Pin(5))
#
# display = ssd1306.SSD1306_I2C(128, 64, i2c)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)
display.text('Hello, World!', 0, 0, 1)
# display.fill(1) 
display.show()
print("After I2C")


led = Pin(2, Pin.OUT)
while True:
    if led.value() == 0:
        led.value(1)
    else:
        led.value(0)
    time.sleep(1)