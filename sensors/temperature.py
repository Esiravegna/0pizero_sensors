from sensors.dht import dht
import datetime
from utils.log import log
log = log.name(__name__)

class TemperatureSensor(object):
	"""
	Just a temperature sensor using the DHT11 library
	"""
	def __init__(self, pin, sensor_type=11):
		log.debug("Initializing DHT11...")
		if sensor_type not in [11, 22]:
			raise ValueError('Invalid Sensor type, must be either 11 or 22')
		self.temperature = False
		self.humidity = False
		self.last_read = False
		self.DHT11 = dht.DHT(pin=pin, sensor=sensor_type)
		log.debug("...DHT11 initialized")

	def update(self):
		result = self.DHT11.read()
		log.debug("Reading DHT11")
		if result.is_valid():
			self.temperature = result.temperature
			self.humidity = result.humidity
			self.last_read = datetime.datetime.now()
			log.debug("DHT11 read OK")	