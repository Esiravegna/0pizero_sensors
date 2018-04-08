from time import time
import paho.mqtt.client as mqtt

from core.config import settings
from utils.log import log

log = log.name(__name__)


class MQTTClient(object):
    def __init__(self, server=settings['MQTT_SERVER'], topic=settings['MQTT_TOPIC'], port=settings['MQTT_PORT'],
                 clean_session=False):
        self.mqttc = mqtt.Client(topic, clean_session=clean_session)
        self.topic = topic
        self.port = port
        self.host = server
        self.lwt = "/{}/alive".format(self.topic)
        self.is_connected = False

        # MQTT callbacks

    def on_mqtt_connect(self, mosq, obj, flags, result_code):
        """
        Handle connections (or failures) to the broker.
        This is called after the client has received a CONNACK message
        from the broker in response to calling connect().
        The parameter rc is an integer giving the return code:
        0: Success
        1: Refused . unacceptable protocol version
        2: Refused . identifier rejected
        3: Refused . server unavailable
        4: Refused . bad user name or password (MQTT v3.1 broker only)
        5: Refused . not authorised (MQTT v3.1 broker only)
        """
        if result_code == 0:
            log.info("Connected to {}:{}".format(self.host, self.port))
            # See also the will_set function in connect() below
            self.mqttc.publish(self.lwt, "1", qos=0, retain=True)
        elif result_code == 1:
            log.error("Connection refused - unacceptable protocol version")
        elif result_code == 2:
            log.error("Connection refused - identifier rejected")
        elif result_code == 3:
            log.error("Connection refused - server unavailable")
        elif result_code == 4:
            log.error("Connection refused - bad user name or password")
        elif result_code == 5:
            log.error("Connection refused - not authorised")
        else:
            log.warning("Connection failed - result code {}".format(result_code))

    def on_mqtt_disconnect(self, mosq, obj, result_code):
        """
        Handle disconnections from the broker
        """
        if result_code == 0:
            log.info("Clean disconnection from broker")
        else:
            log.info("Broker connection lost. Retrying in 5s...")
            time.sleep(5)
            # End of MQTT callbacks
            # With approved

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Signal handler to ensure we disconnect cleanly
        in the event of a SIGTERM or SIGINT.
        """
        # Publish our LWT and cleanup the MQTT connection
        log.info("Disconnecting from broker...")
        self.mqttc.publish(self.lwt, "0", qos=0, retain=True)
        self.mqttc.disconnect()
        self.mqttc.loop_stop()

    def publish(self, subtopic, payload):
        result = False
        if not self.is_connected:
            log.error("Unable to send {}/{} {}, not connected".format(self.topic, subtopic, payload))
        else:
            self.mqttc.publish("/{}/{}".format(self.topic, subtopic), payload, qos=0, retain=True)
            result = True
        return result

    def connect(self):
        """
        Connect to the broker, define the callbacks, and subscribe
        This will also set the Last Will and Testament (LWT)
        The LWT will be published in the event of an unclean or
        unexpected disconnection.
        """
        self.is_connected = False
        # Add the callbacks
        self.mqttc.on_connect = self.on_mqtt_connect
        self.mqttc.on_disconnect = self.on_mqtt_disconnect

        # Set the Last Will and Testament (LWT) *before* connecting
        self.mqttc.will_set(self.lwt, payload="0", qos=0, retain=True)

        # Attempt to connect
        log.debug("Connecting to {}:{}...".format(self.host, self.port))
        try:
            self.mqttc.connect(self.host, self.port, 60)
        except Exception as e:
            log.error("Error connecting to {}:{}: {}".format(self.host, self.port, str(e)))
        self.is_connected = True
        # Let the connection run forever
        self.mqttc.loop_start()
        return self.is_connected
