"""Reads raw data from the CM2016 battery charger over USB"""

__author__ = "Michael Wahler"
__copyright__ = "Copyright 2018, Michael Wahler"
__license__ = "GPLv3"
__version__ = "0.1"
__status__ = "Prototype"

import time
import ConfigParser
import serial


def read_CM2016 ():
	config = ConfigParser.ConfigParser()
	config.read('CM2016.ini')

	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
		port = config.get('USB', 'port'),
		baudrate = 19200,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS
	)

	# print ("ser.isOpen()? {0}".format(ser.isOpen()))

	TIMEOUT_SECONDS = 3

	try:
		timeout = 0

		while timeout < TIMEOUT_SECONDS:

			while ser.inWaiting() > 0:
				buffer = ser.read(127)  # TODO buffer is can be a string or byte array, depending on the Python version

				# print ("{0} character(s) read".format(len(buffer)))

				if 127 == len(buffer):
					ser.close()
					return buffer

			time.sleep(1)
			timeout += 1

		# print ("Timed out after {0} seconds.".format(timeout))
		ser.close ()
		raise Exception ("The connection to {0} timed out after {1} s.".format (config.get('USB', 'port'), timeout))

	except Exception as x:
		# print (str(x))
		ser.close()
		raise x
	
