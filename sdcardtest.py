import os, machine

# NOT WORKING >..

import sdcard

# Wiring SD card module <-> ESP8266 (GPIO):
# GND <-> GND
# DO/MISO <-> MISO (12)
# DI/MOSI <-> MOSI (13)
# CLK/SCK <-> SCK (14)
# CS <-> CS (15)
# VCC <-> VCC 3.3V/5V

# sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))  # hard reset required after wiring


# MISO - 7
# MOSI - 8
# SCK - 6
# CS - 11
#sd = sdcard.SDCard(machine.SPI(1), machine.Pin(11))  # hard reset required after wiring



cs = machine.Pin(15, machine.Pin.OUT)

spi = machine.SPI(
    1,
    baudrate=1000000,
)

sd = sdcard.SDCard(spi, cs)

print(sd)

vfs = os.VfsFat(sd)   # is this required?
os.mount(vfs, '/sd')   # or '/' if you did the umount command before


# os.mount(machine.SDCard(), "/sd")

#os.umount('/')       # only if you want to unmount flash (NOT REQUIRED!)

#os.listdir()         # you'll see a new '/sd' folder
#os.statvfs('/sd')	 # size of sd card = [0]*[2] bytes (free: [0]*[3])
os.chdir('sd')        # to change directory (if you kept '/')
os.listdir()         # you'll see the sd card's contents (or listdir('/sd') from outside)