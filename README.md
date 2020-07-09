# Plant, temperature and humidity monitor with optional database and notifications
:::info 
Most of us have plants in our homes and I know I tend to forget to give them their essentials: water and a pleasant living area. 

This tutorial aims to get you through building a plant monitoring system with additional temperature and humidity monitoring. The sensors are connected to a LoPy4 who then communicates through MQTT. The data can be presented on a dashboard using Adafruit or using Grafana and storing the data on InfluxDB for further analysing (on a Raspberry Pi).
:::
##### By: Leyla Wejdell (lw222te)


![](https://i.imgur.com/Wy6vRAF.png)
*Depending on your experience: 
Part 1 takes approx. 2-3 hours to complete. 
Part 2 takes approx. 3-5 hours*

[TOC]

# Objective
I chose to make this project *because* I want to be able to monitor my six plants, collect data from them and get notifications when they need water. Adding a temperature and humidity sensor creates extra value for further analysing. I also wanted something I can control remotely. Having fun making something practical and learn more about transport protocols.
The *purpose* of this project is to gather data and monitor your plants soil moisture, room temperature and humidity. Visualizing this with some awesome graphs.
By adding a database and collecting sensordata *we can learn* about the environment our plant-babies live in. In the end, through the data, we will learn what conditions might be the best for a specific plant.

# Hardware
The main components you need for configuring are a PC or laptop, a monitor, keyboard, mouse, MicroSD card reader and a Wi-Fi connection. Also, two extra mobile phone charger – bricks.

## Components for Part 1

|Devices|Link|Description|Price|
| -------- | -------- | -------- |-------- |
|LoPy4*| [link](https://pycom.io/product/lopy4/)|Quadruple network development board, runs micropython|34,95€|
|Expansion board 3.0| [link](https://pycom.io/product/expansion-board-3-0/) | For using GPIO, connecting sensors etc|16€|
|**Sensors**||||
| FC-28 ** | [link](https://cutt.ly/moBXgZv)| Measures voltage between to capacitors, giving us soil humidity| 2,8€ *6
| DHT11 | [link](https://cutt.ly/0oBXl3s)| Measures temperature and air humidity    |4,7€|
|**Essentials**| | | |
|Micro USB cable|[link](https://www.electrokit.com/produkt/usb-kabel-a-hane-micro-b-5p-hane-1-8m/)|3,5€|
|Breadboard|[link](https://cutt.ly/qoBXQLo)|For connecting sensors and the LoPy4|7€|
|Jumper wires M/M|[link](https://cutt.ly/YoBXUX9)|To connect components|3€|
|Jumper wires F/M|[link](https://cutt.ly/KoBXAui)|To connect components / extend soil sensors|3€|
||||~90€ |
*Can also be [WiPy](https://pycom.io/product/wipy-3-0/) or the [Node MCU](https://cutt.ly/1oBXG6C), depending on your budget and knowledge
** If you have a higher budget I recommend getting [capacitive sensors](https://cutt.ly/AoBXXTl), which have a longer lifespan

## Components for Part 2
|Devices|Link|Description|Price|
| -------- | -------- | -------- |-------- |
|Raspberry Pi Zero with essentials |[link](https://www.electrokit.com/produkt/raspberry-pi-zero-w-essentials-kit/) | Minicomputer, runs backend components and triggers|19€|
|**Essentials**| | | |
|Micro SD Card|[link](https://cutt.ly/poBXvEj)| For installing software on the RPi|9,9€|
|Micro USB cable|[link](https://www.electrokit.com/produkt/usb-kabel-a-hane-micro-b-5p-hane-1-8m/)|For powering the device|3,5€|
||||~125€

# Computer and device setup
To be able to communicate with the devices you need some software on your computer. I used atom for writing the code. The Atom pymakr plugin will also help us upload the code to the LoPy4. You can also use Visual Studio code if you prefer it. If you want to use a Raspberry Pi it is preferable to download a SSH client for coding and configuring. 



1. Installing [Atom and the Pymakr plugin](https://docs.pycom.io/pymakr/installation/atom/)
2. If on windows: Installing [PuTTY](https://www.putty.org/) This tool makes it possible to communicate with the Raspberry Pi without connecting peripherals. If you’re on mac or Linux, you don’t need any extra software for SSH.
3. Installing extra drivers [for windows/linux/macOS]( https://docs.pycom.io/gettingstarted/installation/drivers/)

 
## Setting up the LoPy4
Before we get started, we should update the firmware of the expansion board to prevent any bugs from messing with our project. It is recommended but not mandatory. Follow [this guide](https://docs.pycom.io/pytrackpysense/installation/firmware/)
After we have flashed the board, we connect the LoPy4 to the expansion board like this:
![](https://i.imgur.com/EKTw4bF.png =300x280)
Now we can connect the device to our computer using a Micro USB cable. **Make sure we are not running atom at this point**
1. Create an account over at [pybytes](https://pybytes.pycom.io) and log in
2. Continue by [adding the Pycom device to pybytes](https://docs.pycom.io/pybytes/connect/) 
3. [Provisioning and flashing your device via USB](https://docs.pycom.io/pybytes/connect/quick/) This guide will also get us through the very important part of **updating the firmware of the LoPy4**
4. After the firmware update is done, I recommend following this [RGB Blink Example](https://docs.pycom.io/gettingstarted/programming/first-project/) to make sure everything went fine and Atom can communicate with our Pycom device. 
5. Make sure to try the last step in the example in step 4 since this is how we will upload the project to the pycom device later.

## Setting up the Raspberry Pi Zero
If you're not familiar with the Raspberry Pi devices, check [this](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) out.
For our backend services we are using the Raspberry Pi Zero. It runs everything off of the Micro SD card. To get started we need to download the [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) and then the [Raspberry Pi OS Lite image](https://www.raspberrypi.org/downloads/raspberry-pi-os/) and follow the full [installation guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).

After the Micro SD card is flashed, we can insert it to the device and then connect your peripherals and connect the power cable
![](https://i.imgur.com/j37hkjt.png =450x280)


1. Set up the device so it [connects to our Wi-Fi](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md). 
2. Since we want to be able to use the devices simultaneously we need to [configure the device with SSH ](https://www.raspberrypi.org/documentation/remote-access/ssh/). After this we can go back to our main PC and fiddle on
When we use SSH we can copy and paste the code and commands directly to the raspberry pi.
## Setting up your Adafruit Account
1. Sign up for a free account over at [Adafruit IO](https://accounts.adafruit.com/users/sign_up)
2. If you’re doing 6 soil moisture sensors, [set up some feeds](https://learn.adafruit.com/adafruit-io-basics-feeds/creating-a-feed) with the names of the pins, to keep track of which plant is which and their respective values. 
3. Like this: ![](https://i.imgur.com/7jwLiAw.png)
4. Grab the Adafruit KEY![](https://i.imgur.com/5BZqtZy.png)
5. Copy the Active key and store it somewhere for the moment. We will add it in the code later.
# Putting everything together 
After a lot of testing I found that connecting the soil moisture sensors individually worked best. Since they are not capacitive this will help the durability because we will only power one sensor at a time.
The LoPy4 has some [restrictions to which pins we can use](https://docs.pycom.io/firmwareapi/pycom/machine/pin/), but the pins mentioned in the table below worked for me

## Circuit Diagram
![](https://i.imgur.com/zTgm5wU.png)
The breadboard is used to connect the ground cables together and help us put the rest of the components together a bit easily.
The circuit board of the soil moisture sensors and the DHT11 sensor connect to the breadboard and are then extended with the Male/Male jumper wires into the pycom device.

The Male/Female wires are used between the soil moisture circuit board and the "legs". Here we could add a few extra to enable them to reach plants further away than 20cm, just make sure we got + and - right
I chose to make my build a bit more compact using a smaller breadboard but it's the same idea as the circuit diagram, only folded together. I also dug up my soldering iron and some wires that I used to extend the soil sensor board and "legs" to 120cm.
![](https://i.imgur.com/coyVskD.jpg)

Here are my results and a video of me struggling with all the wires

![](https://i.imgur.com/VusdI82.jpg)

<iframe width="560" height="315" src="https://www.youtube.com/embed/SX3KGmY5pao" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> 

#### Pins used for the sensors
![](https://i.imgur.com/oiGpCU9.png)
If you don’t need/want to use 6 moisture sensors, you can just connect the pins respectively and match it with the list in [main.py](https://github.com/lwej/Pycom-Soil-Monitor/blob/master/pycom/main.py)
### Discussion - electricity
Both the LoPy4 and the Raspberry pi are not power-hungry devices. I will not be discussing the Raspberry Pi's consumption since this device is always meant to be powered on at home.
I chose the LoPy4 since I plan to experiment and take this project outdoors, communicating with LoRa and running off a battery. Right now, it runs off a direct power connection. I skipped a few classes on physics and electricity but with the current conditions we have some values to play with [in theory](http://www.of-things.de/battery-life-calculator.php): 

##### FC-28: 35mA (x6)
##### DHT11: 0.3mA 
##### LoPy4 on WiFi: 110mA 

Running off a 10000mAh power bank, only measuring once an hour and deep sleeping the rest, it could run for around two months

# Platform
There are a bunch of different platforms available. Some who might be free but lack configurability and some that cost more and are configurable to the bone. 
In this project we are using:
* **Adafruit IO** For their easy dashboard and MQTT broker
* **Grafana** Open source with endless configurability, easy to set up alerts, notifications to various channels and easy connection to:
* **InfluxDB**. Open source time series database, simple and not too complicated to configure to collect MQTT data
All of them are free to use and right now they fulfil all requirements. There are no subscription fees in this project.
I found that Adafruit IO was enough for the purpose of this project, the Pycom documentation mentions Adafruit a few times and refers to handy guides. They offer a nice layer of security for MQTT communication.
Grafana and InfluxDB have been buddies for a while. It is easy to set up the InfluxDB against Grafana and configuring alerts for your dataflow.  They are also available to install on the Raspberry Pi. 

## Discussion

If I would’ve put more time into research I would have found that a Raspberry Pi 4 would have been more suitable for this project, because it supports the TIG-stack and running docker, which makes things a bit easier. 

I looked in to Balena Cloud, thethingsio, Ubidots and they all have their perks, but it often led to needing to pay for a subscription in the long run. The Balena Cloud is an interesting platform but has a higher learning curve. 

If we want to add more sensors in the future, we need to reconsider the use of Adafruit, since it limits the amount of topics/feeds we can pub/sub to. 

*If you're not that interested in running your own database you could build only the first part, and if you have the cash, you can pay for Adafruit IO plus, which adds alerts/triggers to the relevant topics.*

# The Code
1. Download the code from the [Github Repository](https://github.com/lwej/Pycom-Soil-Monitor)
## Code on the LoPy4
1. Make sure your Pycom device is recognized in Atom, [RGB Blink Example](https://docs.pycom.io/gettingstarted/programming/first-project/)
2. Before we start sending values through to the Adafruit broker it would be awesome to see some values, right?
3. Choose the **test run** folder as the project folder by choosing the menu item File > Open Folder and select a directory from the dialog.
4. Upload the project to your device
5. Run [test.py]( https://github.com/lwej/Pycom-Soil-Monitor/blob/master/test%20run/test.py) to see if you are getting some values from the sensors, these will be shown in the terminal
6. Example: ![](https://i.imgur.com/qZt1MCg.png)
7. The soil sensor values are between ~250-999 mV, where the lowest value means they are moist and 999 is absolutely dry
8. You can follow the process by looking at the sensors circuit board which lights up during the measuring. The DHT11 sensor does not light up.
10. If everything looks alright, delete the "test run" as project folder and replace it with the **pycom** folder
7. Choose the **pycom** folder as the project folder. Choose the menu item File > Open Folder and select a directory from the dialog.

### Configurations and explanations – [main.py](https://github.com/lwej/Pycom-Soil-Monitor/blob/master/pycom/main.py)
```python
import time                   # Allows use of time.sleep() for delays
import ubinascii              # Following Adafruit MQTT configure
import machine                # Interfaces with hardware components
from dht import DHT           # Library for the DHT11 Sensor
from machine import Pin       # Pin object to configure pins
from machine import ADC       # ADC object to configure reading values
from umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
```
Here are the pins we are using
```python
# Pins we want to read from
ao_pins = ['P20', 'P19', 'P18', 'P17', 'P16', 'P15']
# Pins we want to turn on/off
vcc_pins = ['P4', 'P5', 'P9', 'P10', 'P11', 'P12']
```
In this section we need to add our credentials. Replacing:
user_name with the adafruit io username you chose
adafruit_key with your Adafruit Active key
This configuration makes it possible to send data using MQTT

```python
# Adafruit details
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "user_name"
AIO_KEY = "adafruit_key"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
AIO_TEMPERATURE_FEED = "temperature"
AIO_HUMIDITY_FEED = "humidity"
AIO_SOIL_FEED = "soil"
```

```python
#Here we set up the ao_pins as in-”put” to read the values 
for p in ao_pins:
    set = Pin(p, mode=Pin.IN)
```
Creating an ADC object makes it possible for the LoPy4 to convert the analog signal that the soil moisture sensor sends to a digital signal so we can read the value.
``` python
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
``` 
The DHT11 has its own library to help read the measurements. We are just making sure to read the values as long as they are valid, then sending them back in a variable
```python
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
```
In the main section we configure an MQTT client, connect it and then we
Iterate over the soil sensor pins and publish the values to their respective feed which is "soil" + "pin number". The feed we are publishing to will be printed in the terminal
The only data conversion we need to do is making sure we are sending string values, since this is one acceptable data format to publish. 
```python
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
    time.sleep(60 * 10)
```
In the last few rows, we set up the main function to run every 10 minutes. While you are testing you might want to change time.sleep(seconds) to whatever suits you. 


There are some additional files besides [main.py](https://github.com/lwej/Pycom-Soil-Monitor/blob/master/pycom/main.py). To use MQTT we need a specific library which is the umqtt.py file from the [Adafruit_IO Python Library](https://github.com/adafruit/Adafruit_IO_Python). The DHT11 sensor also uses a library which is located at lib/dht.py
**Don't forget to save your changes**
**Now we can upload the project to the Pycom device.** [Example](https://docs.pycom.io/gettingstarted/programming/first-project/)

After this part you can [create a dashboard in adafruit io]( https://learn.adafruit.com/adafruit-io-basics-dashboards/creating-a-dashboard) and check to see that your MQTT client is publishing values. 

## Code on the Raspberry Pi

**Basic configurations**
Since we are running **buster lite** we need some things that aren't automatically there.

```
sudo apt install python3                 # Installing python
sudo apt-get install python3-pip         # Installing pip for python modules
sudo apt-get install libfontconfig       # Necessary for running Grafana
sudo apt update && sudo apt upgrade -y   # Make sure we are fully updated
```

Moving on to installing InfluxDB and Grafana. I wanted to write this part myself, but the length of this report would greatly exceed the recommendation. So I will give full credit to diyi0t and refer you to following their guide on [Installing InfluxDB and Grafana on Raspbery Pi](https://diyi0t.com/visualize-mqtt-data-with-influxdb-and-grafana/) 
 **Note**: We will use a customized **[MQTTToInfluxDBBridge.py](https://github.com/lwej/Pycom-Soil-Monitor)** available at the github repository
**Make sure to update the code with your credentials**

### Remote access(optional)


If you want to see your **Grafana** graphs while you are not connected to your home network, you can easily install dataplicity and run a web server on the raspberry pi. Register at https://www.dataplicity.com/ and follow the steps to connect your device to dataplicity.

#### Installing web server

```
sudo apt-get install nginx
sudo netstat -an | grep LISTEN | grep :80
```
The output should look something like this:
```
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN
tcp6       0      0 :::80                   :::*                    LISTEN
```
If it does not, run:
`sudo service nginx restart`

#### Configure Grafana to show at your dataplicity device link
`sudo nano /etc/nginx/sites-available/default`
Add the following to the server block:
```
server {
  listen 80;
  root /usr/share/nginx/html;
  index index.html index.htm;

  location / {
   proxy_pass http://localhost:3000/;
  }
}
```
After this is done, you go to https://www.dataplicity.com/ , click on your device and enable wormhole.
Now you get access to the same content you would get if you were to connect to raspberrypi:3000 in your browser.

    
# Connectivity
### Wireless protocols
We are sending data over WiFi, the LoPy4 is connected to the same WiFi as the Raspberry Pi Zero. Since they are both in my home. The opportunity to use LoRa is always there, making the project transferable outdoors.
### Frequency of data transfer
The frequency of the data being sent can be tweaked, right now it sends data every tenth minute. Since we are using a free Adafruit IO account, it is limited to 30 data points per minute. Meaning we are not allowed to send data that often (**note**: this can lead to a ban). 
### Transport protocols 
The way the transferring works is using the Adafruit IO MQTT broker that is configured using our Adafruit active key and username, adding a layer of security to prevent anybody from publishing or subscribing to our feeds.
The Pycom device publishes data to a feed and both the Raspberry Pi and Adafruit dashboard are subscribed to the feed/topic.
### Elaboration
MQTT in IoT is almost a must, it is a simple transfer protocol, and everybody should try it out at some point. Using Adafruit's broker makes it possible to keep the current settings on the Raspberry Pi and just moving the LoPy4 and sensors to another location. The Pi will always be able to receive the data. If we set up the LoPy4 to communicate through another wireless protocol, we need to consider some slight power consumption changes.

My initial thought was to set up my own MQTT broker and thus running it locally, preventing any other external connections for security reasons.

Running InfluxDB and Grafana locally on the raspberry pi makes it possible to run your own MQTT broker or other wireless communication protocols such as webhooks, sockets etc.

As for now, both devices are wall-powered and connected to my home wifi, no need to worry about battery-life just yet.
![](https://i.imgur.com/Qf68bGg.png)



# Presenting the data
The data is easily accessible through https://io.adafruit.com/user-name/dashboards

![](https://i.imgur.com/kSUnczw.png)


or via Grafana at http://raspberrypi:3000/ or http://dataplicity-device-link.io/

![](https://i.imgur.com/V7r7huZ.png)
## Data storage frequency 
The data is saved in InfluxDB as soon as it is received through MQTT. Almost instantly after the LoPy4 publishes the data the MQTTToInfluxDBBridge.py script handles storing the received data in our sensor_data database. This is then easily accessible using Grafana who connects to InfluxDB within a few clicks in the UI.


Adafruit and dataplicity are accessible from anywhere, with the small difference that adafruit only stores data for 30 days (free account) and through our Raspberry Pi, we can gather data for 600 years before it is full. **Not considering the durability of the device and MicroSD card.**
###### Running two weeks, sending data every five minutes for this project I've stored 660 KB in the database, meaning we can send data every five minutes for a hundred years without getting up to 2GB

Both the dashboards are showing the data received in real-time. Grafana gives us the opportunity to browse all the stored data.
## Visualization 
Create a dashboard
![](https://i.imgur.com/L2LkkgS.png)

### Soil data
Adding a panel
![](https://i.imgur.com/ynBD58R.png)
Then choosing **Add Query**

![](https://i.imgur.com/jdMoz4r.png)

I set up individual panels for every plant, giving them relevant names.

![](https://i.imgur.com/GjuhTRb.png)
![](https://i.imgur.com/eHQfe2R.png)
![](https://i.imgur.com/kRw4D3M.png)
You can then duplicate them, changing the measurement and names
![](https://i.imgur.com/sqzwzkD.png)

I also set up one for *all* the plants
![](https://i.imgur.com/VYlx83d.png)
It is noticable when I watered my Chillies and Avocado no.5
The reason Avocado no.1 has such high values is simply because it has a bigger pot. Meaning the water runs through it faster and the topsoil is relatively dryer. Exciting!
![](https://i.imgur.com/Hhuv22Z.png)
### Humidity and temperature
![](https://i.imgur.com/Q57rI7D.png)
![](https://i.imgur.com/8qUP6h9.png)
![](https://i.imgur.com/RZvh8Tl.png)

You can then click and drag to put the panels anywhere you like.

## Triggers of the data
Grafana makes it really easy to enable alerts for our data flow. I chose alerts through Discord and Google Chat. If you want something else, [check this documentation](https://grafana.com/docs/grafana/latest/alerting/notifications/)

Save your changes and go to the main dashboard
Select Notification channels and add a New channel
![](https://i.imgur.com/mLSu0t7.png)
For discord, you need a server, I created one called Soil Monitor Server, In the server settings you can create a webhook and just copy it into Grafana. [Discord: how to create a webhook](https://support.discord.com/hc/sv/articles/228383668-Anv%C3%A4nda-Webhooks)
![](https://i.imgur.com/4FUIA3x.png)

Now test the notification by pressing Send Test.
![](https://i.imgur.com/wWDgcUs.png)

Now we can go back to the panels we want to enable alerts for.
The value of 950 means the plant is extremely dry. That is when I want a notification to water since that would mean I completely forgot.
![](https://i.imgur.com/JD77MSz.png)

And testing this by pulling the soil moisture sensor out of the plant.
![](https://i.imgur.com/np5Acf1.png)



## Elaboration

Using InfluxDB was an obvious choice because it is simple since it is based on time series. It is open source and available for most devices. It was easy to install on the Raspberry Pi and the connection to Grafana was really easy. You just choose InfluxDB as a data source and fill out your credentials. I have no previous knowledge of databases and the option to just choose queries using a drop-down menu really made it simple.


# Finalizing the design

To complete this DIY project, I found a plastic container, cut some holes in it and threw all the electronics inside, holding them together with some double-sided tape.

## LoPy4
![](https://i.imgur.com/nDRodoa.jpg)

The clear plastic is obviously optional, but I like to see the messy-ness to keep the DIY spirit shining through. But it keeps everything as contained as possible. 

![](https://i.imgur.com/7WkDBfK.jpg)


Put the soil sensors in the plants
![](https://i.imgur.com/Mrx51oM.jpg)

![](https://i.imgur.com/97TVq4S.jpg)

Do some cable management.
![](https://i.imgur.com/J8nbreb.jpg)

## Raspberry Pi
Now, convienently the RPi zero fits just perfectly in one of the plastic boxes that contained the LoPy4 or the Expansion board. I just cut a hole through one of them and used some double-sided tape to hold the pi in place.

![](https://i.imgur.com/RqxAvty.png)

Throw the Pi wherever it has WiFi access and power

![](https://i.imgur.com/blPqHWu.jpg)


## Thoughts

Overall, the project build went alright, there were some things I should've thought of. For example, the possibility to use a Raspberry Pi 4 instead of a Zero, enabling easier use of docker and the full TIG-stack.

My initial plan was to use the RPi as an actuator, connecting pumps to it, but the delivery time of the pumps was over 5 weeks. This is a possible improvement to be made. The RPi's GPIO pins are easy to program and given the script we're already running; it shouldn't be so hard to implement.

It would also be logical to install a light sensor for measuring the amount of light for the plants.


My main issues were: 
* Finding a reliable guide for installing grafana and influxdb on the RPi zero, this was the most time consuming. Configuring the LoPy4 itself was straight forward once I read the ADC and Pin in the pycom documentation.
* Finding an appropriate micropython library for MQTT communication for the LoPy4. Initially I tried the paho library but ran in to quite a few issues.
* Overall MQTT formatting, but that is easily solved by doing proper research. I rushed into it thinking paho projects from earlier assignments was enough. 

And also, next summer, this project will go outdoors, and I will have the opportunity to experiment further with LoRa to measure plants and temperature inside of a greenhouse.

# Video presentation
<iframe width="560" height="315" src="https://www.youtube.com/embed/KFwPk6DpuYY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

###### tags: `IoT`, `DIY`,`plant monitor`,`soil moisture`,`DHT11`,`FC-28`, `Pycom`,`temperature monitor`,`LoPy4`,
