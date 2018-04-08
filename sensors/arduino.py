import smbus
import datetime
from utils.conversion import little_endian_byte_to_int
from utils.log import log
log = log.name(__name__)

"""
Arduino Gas Sensor
"""

class ArduinoGasSensor(object):
	def __init__(self, address=0x09, device=0):
		log.debug("Initializing Arduino Gas Sensor...")
		self.address = address
		self.device = device
		self.bus = smbus.SMBus(device)
		log.debug("...Arduino Gas initialized")
		self.MQ2Value = False
		self.MQ135Value = False

	def update(self, payload_size = 4):
		#log.debug("probing the sensor...")
		response = self.bus.read_i2c_block_data(self.address,0, payload_size)
		self.MQ2Value = little_endian_byte_to_int(response[2:])
		self.MQ135Value = little_endian_byte_to_int(response[:2])
		#log.debug("sensor.probed")



	