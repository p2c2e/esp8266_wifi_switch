import esp
import network
from machine import Pin
import socket
import sys

from machine import I2C
import sh1106

# Connections
# USB for power
# D1 -> SCK
# D2 -> SDA
# 3V3 -> VCC
# GND -> GND
# D6 -> LED+ -> Resistor -> GND

print("Before I2C")
i2c = I2C(sda=Pin(4), scl=Pin(5))
# i2c = I2C(0)
#
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)
display.invert(0)
#display.text('Hello, World!', 0, 0, 1)
#display.show()
print("After I2C")

# minicom -D /dev/cu.SLAB_USBtoUART -b 115200

ip = "X"
display.fill(0)
display.text("Connecting...", 0,0, 1)
display.show()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('SSID', 'password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    return sta_if.ifconfig()[0]

ip = do_connect()
print(ip)

display.fill(0)
display.text("IP: "+ip, 0,0, 1)
display.show()

print("Step 0")

led = Pin(2, Pin.OUT) # There are two LEDs 2, 16

#myled = Pin(0, Pin.OUT) # GPIOZero - D3 pin
#myled.value(0)

relay_pin = Pin(15, Pin.OUT) # GPIO15 - D8 pin
# NOTE Had issues due to messing with Tx,RX pins and serial...
relay_pin.value(0) # High implies - relay is open/off
led.value(1) # Active low - led will be off

print("Step 1")

def web_page():
    if led.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"
    html = """<html><head> <title>Wifi Switch</title> <body> <h1>ESP Web Server</h1>  
    <a href='/?led=off'>Off</a><br/><a href='/?led=on'>On</a><br>
    </body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print("Step 2")

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        
        if led_on == 6:
            print('LED ON')
            led.value(0)
            #myled.value(1)
            relay_pin.value(1) # active low / relay on
            display.fill(0)
            display.text("IP "+ip, 0,0, 1)
            display.text("ON", 10, 10, 1)
            display.show()
        if led_off == 6:
            print('LED OFF')
            led.value(1)
            #myled.value(0)
            relay_pin.value(0) # relay off
            display.fill(0)
            display.text("IP "+ip, 0,0, 1)
            display.text("OFF", 10, 10, 1)
            display.show()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print("Timeout? "+e)
