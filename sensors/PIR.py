from datetime import datetime
from pyA20.gpio import gpio
from utils.log import log
log = log.name(__name__)

class PIRSensor(object):
	def __init__(self, pin):
		log.debug("Initializing PIR...")
		self.pin = pin
		gpio.setcfg(self.pin, gpio.INPUT)
		self.motion = False
		self.last_update = False
		log.debug("...PIR initialized!")

	def update(self):
		reading = gpio.input(self.pin)
		log.debug("Reading PIR : {}".format(reading))
		if reading:
			self.motion = 1
		else:
			self.motion = 0
		self.last_update = datetime.now()
