import threading

from pyA20.gpio import gpio

from core.config import settings
from sensors.MQX.MQ135 import MQ135
from sensors.MQX.MQ2 import MQ2
from sensors.PIR import PIRSensor
from sensors.arduino import ArduinoGasSensor
from sensors.temperature import TemperatureSensor
from utils.log import log
from utils.mqtt import MQTTClient

log = log.name(__name__)


class SensorsController(object):
    """
   Sensors controller class, polls the sensors and sends the payloads
    """

    def __init__(self):
        log.info("Initializing controller...")
        gpio.init()
        self.arduino = ArduinoGasSensor()
        self.mq2 = MQ2(self.arduino)
        self.mq135 = MQ135(self.arduino)
        self.temperature = TemperatureSensor(pin=settings['OPI_ZERO_SENSORS_PIN_DHT'])
        self.movement = PIRSensor(pin=settings['OPI_ZERO_SENSORS_PIN_PIR'])
        self.mqtt = MQTTClient()
        self.current_motion = 0
        self.current_t = False
        self.current_h = False
        self.thread_motion = threading.Timer(settings['READ_MOTION_INTERVAL'], self.send_motion_reading)
        self.thread_gas = threading.Timer(settings['READ_GAS_INTERVAL'], self.send_gas_reading)
        self.thread_temperature = threading.Timer(settings['READ_TEMP_INTERVAL'], self.send_temperature_reading)
        log.info("...controller ready")

    def start(self):
        """
        Runs the neverending loop for MQTT
        """
        with self.mqtt as m:
            m.connect()
            self.thread_gas.start()
            self.thread_motion.start()
            self.thread_temperature.start()
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                break

    def send_gas_reading(self):
        log.debug("Sending gas data")
        mq2_reading = self.mq2.MQPercentage()
        reading = mq2_reading.copy()
        reading.update(self.mq135.MQPercentage(self.current_h, self.current_h))
        for key, value in mq2_reading.items():
            self.mqtt.publish(key, value)

    def send_temperature_reading(self):
        log.debug("Sending temp data")
        self.temperature.update()
        self.mqtt.publish('temperature', self.temperature.temperature)
        self.mqtt.publish('humidity', self.temperature.humidity)
        self.current_h = self.temperature.humidity
        self.current_t = self.temperature.temperature

    def send_motion_reading(self):
        self.movement.update()
        reading = self.movement.motion
        if reading != self.current_motion:
            log.debug("Sending motion data")
            self.current_motion = reading
            self.mqtt.publish('PIR', self.current_motion)
