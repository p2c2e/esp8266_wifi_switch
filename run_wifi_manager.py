from wifi_manager import WifiManager
from machine import Timer, Pin

wifi_waiting_led_timer = Timer(-1)
led = Pin(2, Pin.OUT) # There are two LEDs 2

def led_timer_fn(t):
    led.value(not led.value())

wifi_waiting_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=led_timer_fn)


wm = WifiManager()

print("Connecting...")
wm.connect()
print("Connected")
wifi_waiting_led_timer.deinit()
led.value(1) # Turn off - in-case it was on ...