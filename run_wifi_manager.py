from wifi_manager import WifiManager
from machine import Timer, Pin

#
# On Wemos D1 Mini -
# - the GPIO4 is connected to GND via a push button 
# 1. If button is pressed down during boot, wifi details are deleted
# 2. If wifi details are missing - we can connect via AP and 192.168.4.1 to provide credentials
# 3. If wifi details are present, it connects to the last connected network
#
led = Pin(2, Pin.OUT) # There are two LEDs 2

delete_pin = Pin(4, Pin.IN, Pin.PULL_UP) # Delete wifi.dat if GPIO4 pin is held to GND during startup
if(delete_pin.value() == 0): # if pulled down...
    import os
    import utime
    try:
        os.remove('wifi.dat')
    except Exception as e:
        print(e)
    secs = 3
    for _ in range(secs/0.1):
        led.value(not led.value())
        utime.sleep(.1)


wifi_waiting_led_timer = Timer(-1)


def led_timer_fn(t):
    led.value(not led.value())

wifi_waiting_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=led_timer_fn)


wm = WifiManager()

print("Connecting...")
wm.connect()
print("Connected")
wifi_waiting_led_timer.deinit()
led.value(1) # Turn off - in-case it was on ...

print("IP is {0}\n".format(wm.wlan_sta.ifconfig()[0]))