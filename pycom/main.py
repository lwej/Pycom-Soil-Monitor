import time                   # Allows use of time.sleep() for delays
import ubinascii              # Following Adafruit MQTT configure
import machine                # Interfaces with hardware components
from dht import DHT           # Library for the DHT11 (or DHT22) Sensor
from machine import Pin       # Pin object to configure pins
from machine import ADC       # ADC object to configure reading values
from umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO

ao_pins = ['P20', 'P19', 'P18', 'P17', 'P16', 'P15']
# Pins we want to turn on/off
vcc_pins = ['P4', 'P5', 'P9', 'P10', 'P11', 'P12']
# Adafruit details
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "user_name"
AIO_KEY = "adafruit_key"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
AIO_TEMPERATURE_FEED = "feed_id"
AIO_HUMIDITY_FEED = "feed_id"
AIO_SOIL_FEED = "feed_id"

for p in ao_pins:
    set = Pin(p, mode=Pin.IN)


def moist_sensor(p_in, p_out):
    adc = ADC()
    apin = adc.channel(pin=p_in, attn=ADC.ATTN_11DB)
    p_out = Pin(p_out, mode=Pin.OUT, pull=Pin.PULL_DOWN)
    p_out.value(1)
    time.sleep(2)
    volts = apin.value()
    p_out.value(0)
    time.sleep(2)
    return volts


def humid_temp_sensor(read):
    th = DHT('P23', 0)
    time.sleep(2)
    while read:
        result = th.read()
        while not result.is_valid():
            time.sleep(.5)
            result = th.read()
        temperature = result.temperature
        humidity = result.humidity
        read = False
    return (temperature, humidity)


def main():
    client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
    client.connect()

    for ao, vcc in zip(ao_pins, vcc_pins):
        feed = "feed_id" + ao
        print(feed)
        volts = (moist_sensor(ao, vcc) / 4.096)
        client.publish(feed, str(volts))
        time.sleep(1)

    humid = int(humid_temp_sensor(True)[1])
    client.publish(AIO_HUMIDITY_FEED, str(humid))
    temp = int(humid_temp_sensor(True)[0])
    client.publish(AIO_TEMPERATURE_FEED, str(temp))
    client.disconnect()


while True:
    main()
    time.sleep(60 * 5)
