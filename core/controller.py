from pyA20.gpio import gpio
from time import sleep

from core.config import settings
from sensors.MQX.MQ135 import MQ135
from sensors.MQX.MQ2 import MQ2
from sensors.PIR import PIRSensor
from sensors.arduino import ArduinoGasSensor
from sensors.temperature import TemperatureSensor
from utils.log import log
from utils.mqtt import MQTTClient
from utils.scheduler import Manager

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
        self.temperature.update()
        self.movement = PIRSensor(pin=settings['OPI_ZERO_SENSORS_PIN_PIR'])
        self.mqtt = MQTTClient()
        self.current_motion = -1
        self.current_t = False
        self.current_h = False 
        self.timer = Manager()
        #self.timer_tem = Manager()
        #self.timer_pir = Manager()
        log.info("...controller ready")

    def start(self):
        """
        Runs the neverending loop for MQTT
        """
        with self.mqtt as m:
            m.connect()
            self.timer.add_operation(self.send_gas_reading, float(settings['READ_GAS_INTERVAL']))
            self.timer.add_operation(self.send_motion_reading, float(settings['READ_MOTION_INTERVAL']))
            self.timer.add_operation(self.send_temperature_reading, float(settings['READ_TEMP_INTERVAL']))
            while True:
                sleep(.2)

    def send_gas_reading(self):
        log.debug("Sending gas data")
        mq2_reading = self.mq2.MQPercentage()
        reading = mq2_reading.copy()
        mq_135_reading = self.mq135.MQPercentage(self.current_h, self.current_h)
        reading.update(mq_135_reading)
        for key, value in reading.items():
            self.mqtt.publish(key, round(value,3))

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
            self.mqtt.publish('PIR',reading)
            self.current_motion = reading
