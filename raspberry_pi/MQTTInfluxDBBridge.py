import sys  # Standard python module
from influxdb import InfluxDBClient  # For interacting with InfluxDB
from Adafruit_IO import MQTTClient  # Import Adafruit IO MQTT client

INFLUXDB_ADDRESS = '192.168.X.X'
INFLUXDB_USER = 'User'
INFLUXDB_PASSWORD = 'Password'
INFLUXDB_DATABASE = 'Name of your database'

ADAFRUIT_IO_KEY = 'adafruit_key'
ADAFRUIT_IO_USERNAME = 'user_name'

AIO_TEMPERATURE_FEED = "temperature"
AIO_HUMIDITY_FEED = "humidity"
AIO_SOIL_FEED1 = "soilP20"
AIO_SOIL_FEED2 = "soilP14"
AIO_SOIL_FEED3 = "soilP18"
AIO_SOIL_FEED4 = "soilP17"
AIO_SOIL_FEED5 = "soilP16"
AIO_SOIL_FEED6 = "soilP15"

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


def connected(client):
    client.subscribe(AIO_TEMPERATURE_FEED)
    client.subscribe(AIO_HUMIDITY_FEED)
    client.subscribe(AIO_SOIL_FEED1)
    client.subscribe(AIO_SOIL_FEED2)
    client.subscribe(AIO_SOIL_FEED3)
    client.subscribe(AIO_SOIL_FEED4)
    client.subscribe(AIO_SOIL_FEED5)
    client.subscribe(AIO_SOIL_FEED6)
    print('Connected to Adafruit IO!  Listening for changes...')


def subscribe(client, userdata, mid, granted_qos):
    print('Subscribed')


def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def send_to_influxdb(feed_id, payload):
    json_body = [
        {
            'measurement': feed_id,
            'tags': {
                'feed': feed_id
            },
            'fields': {
                'value': payload
            }
        }
    ]
    influxdb_client.write_points(json_body)
    print('Written to DB')


def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    print('Sending to DB')
    send_to_influxdb(feed_id, payload)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def main():
    _init_influxdb_database()

    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_blocking()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
