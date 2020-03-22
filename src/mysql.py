"""Stores CM2016 measurement to a MySQL/MariDB database"""

__author__ = "Michael Wahler"
__copyright__ = "Copyright 2018, Michael Wahler"
__license__ = "GPLv3"
__version__ = "0.2"
__status__ = "Prototype"

import configparser
import MySQLdb

config = configparser.ConfigParser()
config.read('CM2016.ini')

USERNAME = config.get('MySQL', 'username')
PW = config.get('MySQL', 'password')
DBNAME = config.get('MySQL', 'dbname')


def db_connect():
	db = MySQLdb.connect("localhost", USERNAME, PW, DBNAME)
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# cursor.execute ("CREATE TABLE IF NOT EXISTS `CM2016` (`timestamp` datetime NOT NULL,  `active` tinyint(1) NOT NULL,  `program` varchar(3) NOT NULL DEFAULT '',  `step` int(2) NOT NULL,  `status` varchar(3) NOT NULL DEFAULT '',  `minutes_spent` int(11) NOT NULL,  `mV` int(11) NOT NULL,  `mA` int(11) NOT NULL,  `C` int(11) NOT NULL,  `D` int(11) NOT NULL,  `slot` varchar(1) NOT NULL DEFAULT '',  PRIMARY KEY (`timestamp`,`slot`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")

	return {'db': db, 'cursor': cursor}


def db_create_table ():
	dbx = db_connect()	
	command = "CREATE TABLE IF NOT EXISTS `CM2016` (`timestamp` datetime NOT NULL,  `active` tinyint(1) NOT NULL,  `program` varchar(3) NOT NULL DEFAULT '',  `step` int(2) NOT NULL,  `status` varchar(3) NOT NULL DEFAULT '',  `minutes_spent` int(11) NOT NULL,  `mV` int(11) NOT NULL,  `mA` int(11) NOT NULL,  `C` int(11) NOT NULL,  `D` int(11) NOT NULL,  `slot` varchar(1) NOT NULL DEFAULT '',  PRIMARY KEY (`timestamp`,`slot`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
	run_command (command, dbx['db'], dbx['cursor'])
	close_db (dbx['db'])

	
"""Add a CM2016 object to the database"""


def add_CM2016(date, obj):
	for key in obj.slots:
			add_slot(date, obj.slots[key])


def add_slot (date, slot):
	if not slot.is_active():
		return
	
	dbx = db_connect()
	command = "INSERT INTO CM2016 VALUES ('{0}',{1},'{2}',{3},'{4}',{5},{6},{7},{8},{9},'{10}')".format (date, slot.is_active(), slot.get_program(), slot.get_step_raw(), slot.get_status(), slot.get_time_spent_in_minutes(), slot.get_voltage_in_mV(), slot.get_current_in_mA(), slot.get_charged_capacity_in_uAh(), slot.get_discharged_capacity_in_uAh(), slot.name)
	run_command (command, dbx['db'], dbx['cursor'])
	close_db (dbx['db'])


def run_command (command, db, cursor):
	try:
	   # Execute the SQL command
	   cursor.execute(command)
	   # Commit your changes in the database
	   db.commit()
	except Exception as ex:
	   # Rollback in case there is any error
	   db.rollback()


def close_db(db):
   # disconnect from server
	db.close()
