import os

settings = {
    'MQTT_SERVER': os.environ.get('MQTT_SERVER', 'localhost'),
    'MQTT_TOPIC': os.environ.get('MQTT_TOPIC', 'some_topic'),
    'MQTT_PORT': os.environ.get('MQTT_PORT', 8883),
    'OPI_ZERO_SENSORS_LOGLEVEL': os.environ.get('OPI_ZERO_SENSORS_LOGLEVEL', 'WARNING'),
    'OPI_ZERO_SENSORS_LOGFILE': os.environ.get('OPI_ZERO_SENSORS_LOGFILE', None),
    'OPI_ZERO_SENSORS_PIN_PIR': os.environ.get('OPI_ZERO_SENSORS_PIN_PIR', 10),
    'OPI_ZERO_SENSORS_PIN_DHT': os.environ.get('OPI_ZERO_SENSORS_PIN_DHT', 19),
    'READ_MOTION_INTERVAL': float(os.environ.get('READ_MOTION_INTERVAL', '0.5')),
    'READ_GAS_INTERVAL': float(os.environ.get('READ_GAS_INTERVAL', '30.0')),
    'READ_TEMP_INTERVAL': float(os.environ.get('READ_TEMP_INTERVAL', '300.0'))
}
