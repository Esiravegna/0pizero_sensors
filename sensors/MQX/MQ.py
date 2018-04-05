import time
from math import log10
import logging
import sys

from sensors.arduino import ArduinoGasSensor
from utils.log import log
log = log.name(__name__)



class MQ(object):
	"""
	An Abstraction for an MQ sensor which actually reads the values from the Arduino platform
	"""
	# MQ Constants for interpreting raw sensor data
	MaxADC = 4095
	RLOAD = 10000	


	def __init__(self, name, R0, device=ArduinoGasSensor()):
		"""
		The basic sensor constructor
		"""
		log.info("Initializing MQ sensors...")
		self.R0 = R0
		self.device = ArduinoGasSensor
		self.RLOAD = RLOAD
        self.MaxADC = MaxADC
        self.device.update()
		log.info("MQ Initialized")

