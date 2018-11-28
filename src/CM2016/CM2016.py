"""Class definitions for representing the data of the CM2016 battery charger."""


# data format: http://www.leisenfels.com/howto-charge-manager-2016-data-format
# Thanks to Leisenfels UG for documenting the data format
__author__ = "Michael Wahler"
__copyright__ = "Copyright 2018, Michael Wahler"
__credits__ = ["Leisenfels UG"]
__license__ = "GPLv3"
__version__ = "0.2"
__status__ = "Prototype"


PROGRAMS = {
'01': 'CHA',
'02': 'DIS',
'03': 'CHK',
'04': 'CYC',
'05': 'ALV',
'09': 'ERR'
}

def two_byte_hex_to_int (high, low):
	return int ('0x'+high+low, 16)


class CM2016 (object):
	def __init__ (self, buffer):
		device_id = buffer[0:17]	# print (buffer[:6])  # "CM2016"
		slot_1 = buffer[17:35]
		slot_2 = buffer[35:53]
		slot_3 = buffer[53:71]
		slot_4 = buffer[71:89]
		slot_A = buffer[89:107]
		slot_B = buffer[107:125]
		checksum = buffer[125:127]

		#print ("Parsing slots...")
		self.slots = {}
		self.slots["1"] = ChargeSlot ("1", slot_1)
		self.slots["2"] = ChargeSlot ("2", slot_2)
		self.slots["3"] = ChargeSlot ("3", slot_3)
		self.slots["4"] = ChargeSlot ("4", slot_4)
		self.slots["A"] = ChargeSlot ("A", slot_A)
		self.slots["B"] = ChargeSlot ("B", slot_B)
		#print ("CM2016 object successfully initialized.")
	
	def print_me (self):
		for key in self.slots:
			self.slots[key].print_me ()

class ChargeSlot (object):
	# Initializer / Instance Attributes
	def __init__(self, slot_name, slot_data):
		if len(slot_data) != 18:
		 	print ("Error: Slot data must be 18 bytes long")
		 	exit()
		self.name = slot_name
		self.data = slot_data.encode ("hex") # self.data is now 36 bytes long

	def is_active (self):
		is_active_raw = self.data[0:2]
		return True if is_active_raw=='01' else False

	def get_program (self):
		get_program_raw = self.data[2:4]
		try: # look up in dictionary
			return PROGRAMS[get_program_raw]
		except Exception as x:  #not found in dictionary
			return "???"

	def get_step_raw (self):
		return self.data[4:6]
	
	# Program step: 01/03/05/07=charge, 02/04/06=discharge
	def get_step (self):
		return "charge" if self.get_step_raw() in ["01", "03", "05", "07"] else "discharge"

	# 20=empty, "00 xx xx 07" or "00 xx xx 02"=RDY, "00 xx xx 21"=ERR, "01 xx xx 07"=TRI
	def get_status (self):
		get_status_raw = self.data[6:8]
		if self.is_active == True:
			if get_status_raw == '07':
				return 'TRI'
			else:
				return '???'
		else: # self.active == False
			if get_status_raw in ['02','07']:
				return 'RDY'
			if get_status_raw == '21':
				return 'ERR'
			else:
				return "???"
	
	def get_time_spent_in_minutes (self):
		time_spent_low_byte = self.data [8:10]
		time_spent_high_byte = self.data [10:12]
		return two_byte_hex_to_int (time_spent_high_byte, time_spent_low_byte)		
	
	def get_voltage_in_mV (self):
		U_low_byte = self.data [12:14]
		U_high_byte = self.data [14:16]
		return two_byte_hex_to_int (U_high_byte, U_low_byte)
	
	def get_current_in_mA (self):
		I_low_byte = self.data [16:18]
		I_high_byte = self.data [18:20]
		I = two_byte_hex_to_int (I_high_byte, I_low_byte)
		if self.name in ["A", "B"]:
			return I/10
		else:
			return I
		
	def get_charged_capacity_in_uAh (self):
		C_low = self.data [20:22]
		C_high2 = self.data [22:24]
		C_high1 = self.data [24:26]
		
		C = two_byte_hex_to_int (C_high1 + C_high2, C_low)
		if self.name in ['1','2','3','4']:
			return C*10
		else:
			return C
		
	def get_discharged_capacity_in_uAh (self):
		D_low = self.data [26:28]
		D_high2 = self.data [28:30]
		D_high1 = self.data [30:32]
		
		D = two_byte_hex_to_int (D_high1 + D_high2, D_low)
		if self.name in ['1','2','3','4']:
			return D*10
		else:
			return D
		
	def print_me (self):
			print ("-----" * 10)
			print ("Slot {0} ({1})".format(self.name, self.data))
			print ("active: {0}, program: {1}, step: {2}".format(self.is_active(), self.get_program(), self.get_step()))
			print ("status: {0}".format (self.get_status()))
			print ("running for {0} minutes".format(self.get_time_spent_in_minutes()))
			print ("voltage: {0} mV, current: {1} mA".format (self.get_voltage_in_mV(), self.get_current_in_mA()))
			print ("C: {0} mAh".format (self.get_charged_capacity_in_uAh()/1000.0))
			print ("D: {0} mAh".format (self.get_discharged_capacity_in_uAh()/1000.0))

