#!/usr/bin/env python

"""Reads raw data from a CM2016 device over USB, parses it, and displays it."""

__author__ = "Michael Wahler"
__copyright__ = "Copyright 2018, Michael Wahler"
__license__ = "GPLv3"
__version__ = "0.2"
__status__ = "Prototype"

from CM2016 import CM2016
from CM2016 import CMserial
import mysql

import datetime
import sys


# if no command line argument is given, it prints the measurements to the console
# if there is a CL argument 'db' (without quotes), it adds the measurements to the DB
def main():
	try:
		buffer = CMserial.read_CM2016 ()
		cm = CM2016.CM2016 (buffer)
		
		if len(sys.argv) == 1:
			cm.print_me()
		
		if len (sys.argv) > 1:
			if sys.argv[1] == 'db':
				#print ("Adding CM2016 to DB")
				mytime = datetime.datetime.now().isoformat()
				mysql.add_CM2016(mytime, cm)
	except Exception as x:
		print((str(x)))

if __name__ == "__main__":
    # execute only if run as a script
    main()