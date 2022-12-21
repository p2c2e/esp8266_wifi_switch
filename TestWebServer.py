import ESP8266WebServer
import network
from machine import I2C, Pin
import sh1106


###############################
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

################################

# Wi-Fi configuration
STA_SSID = "SSID"
STA_PSK = "password"

# Disable AP interface
ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
    ap_if.active(False)
  
# Connect to Wi-Fi if not connected
sta_if = network.WLAN(network.STA_IF)
if not ap_if.active():
    sta_if.active(True)
if not sta_if.isconnected():
    sta_if.connect(STA_SSID, STA_PSK)
    # Wait for connecting to Wi-Fi
    while not sta_if.isconnected(): 
        pass

# Show IP address
print("Server started @", sta_if.ifconfig()[0])

################################
display.fill(0)
display.text("IP: "+ip, 0,0, 1)
display.show()
################################


################################
relay_pin = Pin(15, Pin.OUT) # GPIO15 - D8 pin
# NOTE Had issues due to messing with Tx,RX pins and serial...
relay_pin.value(1) # High implies - relay is open/off

html = """<html><head> <title>Wifi Switch</title> <body> <h1>ESP Web Server</h1>  
    <a href='/cmd?led=off'>Off</a><br/><a href='/cmd?led=on'>On</a><br>
    </body></html>"""

print("After Relay Pin setup")
################################


# Handler for path "/cmd?led=[on|off]"    
def handleCmd(socket, args, method, contentType, content):
    print('in handleCmd')
    if 'led' in args:
        if args['led'] == 'on':
            handleSwitch(socket, args, method, contentType, content)
        elif args['led'] == 'off':
            handleSwitch(socket, args, method, contentType, content)
    else:
        ESP8266WebServer.err(socket, "400", "Bad Request")

# handler for path "/switch" 
def handleSwitch(socket, args, method, contentType, content):
    print('in handleSwitch')    
    if relay_pin.value() == 1:
        relay_pin.value(0) # active low / relay on
        display.fill(0)
        display.text("IP "+ip, 0,0, 1)
        display.text("ON", 10, 10, 1)
        display.show()
    else:
        relay_pin.value(1) # relay off
        display.fill(0)
        display.text("IP "+ip, 0,0, 1)
        display.text("OFF", 10, 10, 1)
        display.show()
    ESP8266WebServer.ok(
        socket,
        "200", "text/html",
        html)
    
# Start the server @ port 8899
# ESP8266WebServer.begin(8899)
ESP8266WebServer.begin() # use default 80 port

# Register handler for each path
# ESP8266WebServer.onPath("/", handleRoot)
ESP8266WebServer.onPath("/cmd", handleCmd)
ESP8266WebServer.onPath("/switch", handleSwitch)

# Setting the path to documents
ESP8266WebServer.setDocPath("/")

# Setting data for template
# ESP8266WebServer.setTplData(ledData)

try:
    while True:
        # Let server process requests
        ESP8266WebServer.handleClient()
except:
    ESP8266WebServer.close()
