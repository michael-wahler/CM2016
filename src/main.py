#!/usr/bin/env python

"""Reads raw data from a CM2016 device over USB, parses it, and displays it."""

__author__ = "Michael Wahler"
__copyright__ = "Copyright 2018, Michael Wahler"
__license__ = "GPLv3"
__version__ = "0.1"
__status__ = "Prototype"

import time
import serial
import ConfigParser

from CM2016 import CM2016


config = ConfigParser.ConfigParser()
config.read('CM2016.ini')

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port=config.get('USB','port'),
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# print ("ser.isOpen()? {0}".format(ser.isOpen()))

TIMEOUT_SECONDS=3

try:
	timeout = 0
	timed_out = True
	while timeout < TIMEOUT_SECONDS:

		while ser.inWaiting() > 0:
        		buffer = ser.read(127) # TODO buffer is can be a string or byte array, depending on the Python version

			# print ("{0} character(s) read".format(len(buffer)))

			if (len(buffer) == 127):
				cm2016 = CM2016.CM2016 (buffer)
				cm2016.print_me ()
				timed_out = False
		time.sleep(1)
		timeout += 1
	
	if timed_out:
		print ("Timed out after {0} seconds.".format(timeout))

except Exception as x:
	print (str(x))

ser.close()
