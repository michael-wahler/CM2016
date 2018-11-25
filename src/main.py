#!/usr/bin/env python

"""Reads raw data from a CM2016 device over USB, parses it, and displays it."""

__author__ = "Michael Wahler"
__copyright__ = "Copyright 2018, Michael Wahler"
__license__ = "GPLv3"
__version__ = "0.1"
__status__ = "Prototype"

from CM2016 import CM2016
from CM2016 import CMserial

try:
	buffer = CMserial.read_CM2016 ()
	cm = CM2016.CM2016 (buffer)
	cm.print_me()
except Exception as x:
	print (str(x))



