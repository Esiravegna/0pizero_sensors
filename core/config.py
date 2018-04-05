import os

settings = {
	'MQTT_SERVER' = os.environ.get('MQTT_SERVER', 'localhost'),
	'MQTT_TOPIC' = os.environ.get('MQTT_TOPIC', 'some_topic')
	'MQTT_PORT' = os.environ.get('MQTT_PORT', 8883)
 }