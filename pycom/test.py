import time                   # Allows use of time.sleep() for delays
import machine                # Interfaces with hardware components
from dht import DHT           # Library for the DHT11 (or DHT22) Sensor
from machine import Pin       # Pin object to configure pins
from machine import ADC       # ADC object to configure reading values

# Pins to read from
ao_pins = ['P20', 'P19', 'P18', 'P17', 'P16', 'P15']
# Pins we want to turn on/off
vcc_pins = ['P4', 'P5', 'P9', 'P10', 'P11', 'P12']

# Set ao_pins as INput
for p in ao_pins:
    set = Pin(p, mode=Pin.IN)

# Function to read value of a soil moisture sensor
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

# function to read values from the DHT11 sensor
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

# Run ten times
for x in range(10):
    for ao, vcc in zip(ao_pins, vcc_pins):
        volts = (moist_sensor(ao, vcc) / 4.096)
        print(volts)
        time.sleep(1)

    humid = int(humid_temp_sensor(True)[1])
    print(humid)
    temp = int(humid_temp_sensor(True)[0])
    print(temp)
