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

try:
	buffer = CMserial.read_CM2016 ()
	cm = CM2016.CM2016 (buffer)
	cm.print_me()
	print ("Adding CM2016 to DB")
	mytime = datetime.datetime.now().isoformat()
	mysql.add_CM2016(mytime, cm)
except Exception as x:
	print (str(x))



