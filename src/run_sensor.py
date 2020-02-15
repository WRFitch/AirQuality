#!/usr/bin/env python3
import datetime
import logging
import serial 

# this was ~~stolen~~ _adapted_ from stackoverflow https://stackoverflow.com/questions/20892133/storing-string-from-arduino-to-text-file-using-python

arduino_connected = False
logging.basicConfig(filename="logs/" + datetime.date + ".log", level = logging.INFO)

#possible arduino locations
locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3']

for device in locations: 
    try: 
        print "Trying", device
        ser = serial.Serial(device, 9600)
        break
    except:
        print "Failed to connect on ", device

#connect to arduino
while not arduino_connected:
    serin = ser.read()
    arduino_connected = True

#log output to file
while 1:
    if ser.inWaiting():
        x = ser.read()
        print(x)
        logging.info(x)

#close serial connection and text file
logging.close()
ser.close()