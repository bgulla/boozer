# boozer - Kegerator Monitoring Platform 

[![Build Status](https://travis-ci.org/bgulla/boozer.svg?branch=master)](https://travis-ci.org/bgulla/boozer)

```bash
 ____   ___   ___ __________ ____
| __ ) / _ \ / _ \__  / ____|  _ \
|  _ \| | | | | | |/ /|  _| | |_) |
| |_) | |_| | |_| / /_| |___|  _ <
|____/ \___/ \___/____|_____|_| \_\


+---------------+--------------+--------+
|      File     |   Filepath   | Exists |
+---------------+--------------+--------+
|    Database   | ./db.sqlite  |  True  |
| Configuration | ./config.ini |  True  |
+---------------+--------------+--------+
+-------------+---------+
|   Feature   |  Status |
+-------------+---------+
|   Twitter   | enabled |
|     Mqtt    | enabled |
| Temperature | enabled |
|    Slack    | enabled |
|  Scrollphat | enabled |
+-------------+---------+
+-----+------------+--------------------+----------+------------------+
| Tap |    Beer    | Capacity (Gallons) | GPIO Pin | Volume Remaining |
+-----+------------+--------------------+----------+------------------+
|  1  | Test Batch |         5          |    13    |      83.149      |
|  1  | Test Batch |         5          |    14    |      100.00      |
|  1  | Test Batch |         5          |    15    |      100.00      |
|  1  | Test Batch |         5          |    16    |      0.00        |
+-----+------------+--------------------+----------+------------------+
+----------+-----------+
|   Key    |   Value   |
+----------+-----------+
| influxdb |  enabled  |
| database |   boozer  |
|   host   | texas.lol |
|   port   |   31132   |
| username |    None   |
| password |    None   |
+----------+-----------+
+------------+------------+
|  MQTT-Key  | MQTT-Value |
+------------+------------+
|   broker   | texas.lol  |
|    port    |   31353    |
| Connected? | Connected  |
+------------+------------+
+-------------+-------------+
|    Sensor   | Temperature |
+-------------+-------------+
| temperature |   38.175°   |
+-------------+-------------+
2019-05-30 10:55:23,545 flowmeter    INFO     Boozer Intialized! Waiting for pours. Drink up, be merry!
2019-05-30 10:56:25,554 influxdb_client INFO     Influx update pushed. temperature = 37.6134
```




## What is boozer
Kegerator monitoring/volume tracking platform writting in Python. 
 * Track the remaining beer volume of your kegs! Flow sensors keep a running log of your remaining beer volume, using SQLITE.
 * Slack & [Twitter](https://twitter.com/ibuiltabar) functionality. Sharing is caring.
 * Temperature Monitoring via ds18b20 GPIO sensor [or sensors2json microservice/REST](https://github.com/bgulla/sensor2json)
 * IoT functionality with MQTT/Mosquito and InfluxDB.

## Version 2 
* Complete rewrite
* 1-10 flowsensors are now supported
* Custom keg sizes are now supported (5gal, 10gal, etc)
* You can now push metrics directly to InfluxDB and MQTT
* Enhanced UI with configurable verbosity. No more guessing your configuration.
* Temperature sensing can now be done via a GPIO sensor or via a REST call.
* Keg volumes can now be reset without the toolkit
* New docker image. `bgulla/boozer`->`boozerbar/boozer`
* New plug-in supported architecture.
* There are breaking changes. Be sure to convert your configuration to match the new schema.

## Supported Notification Platforms
Boozer can tweet out whenever a new pour event is detected. The following notification platforms are supported:
* Slack (webhook)
![Slack](https://github.com/bgulla/boozer/blob/master/img/slack.png?raw=true)
* Twitter (oauth)
* Untappd Auto-Posting. (I broke this, hoping to fix it soon)

## Supported Monitoring Platforms
* InfluxDB
* MQTT/Mosquitto


## Hardware
The following hardware was used in the inital build of boozer but not necessarily required.
 * [Raspberry Pi](https://www.adafruit.com/product/3055)
 * [Flow Sensors (x4)](https://www.adafruit.com/product/828)
   * [1/2 to 1/4 Adapter (x8)](https://www.amazon.com/gp/product/B00AB5X28G)
 * [ScrollPhat LED Display](https://shop.pimoroni.com/products/scroll-phat) (Optional)
 * [DS18b20 Waterproof Temperature Sensor](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware) (Optional)

![Pouring in motion](https://github.com/bgulla/boozer/blob/master/img/pour.gif?raw=true) 
![Breadboard](https://github.com/bgulla/boozer/blob/master/img/breadboard.jpg?raw=true)
 

## Running in Docker
Simplify deployment with Docker. Instructions for installing docker on RaspberryPi's [here](https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/). Works in Kubernetes, if you're into the whole distributed computing thing. This assumes you have a beginner-level knowledge of Docker. 

```bash
docker run --rm  -d --name="boozer" \
    --privileged \
    -v </path/to/config.ini>:/boozer/config.ini \
    -v </path/to/db.sqlite>:/boozer/db.sqlite \
    -t boozerbar/boozer
```

## Configuration Sample
```
[Boozer]
minimum_pour_vol: 0.075 # Used for testing
logging_level: INFO

[Taps]
tap1_gpio_pin: 13
tap1_beer_name: Test Batch
tap1_gallon_capacity: 5
tap2_gpio_pin: 14
tap2_beer_name: Manor Hill Friends Dont Shake Hands
tap2_gallon_capacity: 5
tap3_gpio_pin: 15
tap3_beer_name: Banquet Beer
tap3_gallon_capacity: 5
tap4_gpio_pin: 16
tap4_beer_name: Seltzer
tap4_gallon_capacity: 5

[Slack]
enabled:True
webhookurl: https://hooks.slack.com/services/<redacted>

[Temperature]
enabled: True
sensor_protocol: ds18b20
#sensor_url: http://10.0.1.48:8888/chillerf
#endpoint: http://10.0.1.48:8888/chillerf

[Twitter]
enabled: True
consumer_key="redacted"
consumer_secret="redacted"
access_token="1549176829-redacted"
access_token_secret="redacted"

[Mqtt]
enabled: True
broker: mqtthost.lol
port: 31353
#username: foo
#password: bar


[Logging]
file: /tmp/beer.log

[Scrollphat]
enabled: True

[Influxdb]
enabled: True
host=influxhost.lol
port=8086
```

## Toolkit
```bash
🍺  pi@bar[/opt/boozer] >docker exec -ti boozer python /boozer/toolkit.py -h
usage: toolkit.py [-h] [--reset-tap RESET_TAP_ID] [--printval] [--temp]
                  [--mqtt]

Example with long option names

optional arguments:
  -h, --help            show this help message and exit
  --reset-tap RESET_TAP_ID, -t RESET_TAP_ID
                        Reset the database value for a tap
  --printval, -p        print all tap volumes
  --temp                print the temperature values
  --mqtt, -m            update the tap values in mqtt broker
  --scrollphat, -s      Test the functionality of the SCROLLPHAT display.
```

### Print Remaining Keg Volumes
```bash
🍺  pi@bar[/opt/boozer] > docker exec -it boozer python /boozer/toolkit.py --printval
Loaded config...
        Database file:  /boozer/db.sqlite
----------------------------------------------------
        Tap 1 | 100.0 remaining
        Tap 2 | 100.0 remaining
        Tap 3 | 100.0 remaining
        Tap 4 | 100.0 remaining
```

### Force-Update MQTT Broker
```bash
🍺  pi@bar[/opt/boozer] > docker exec -it boozer python /boozer/toolkit.py --mqtt
Loaded config...
        Database file:  /boozer/db.sqlite
----------------------------------------------------
[MQTT] updated tap 1
[MQTT] updated tap 2
[MQTT] updated tap 3
[MQTT] updated tap 4
```

### Reseting Taps
The time will come to change out your kegs and rather than editing sqlite directly, use the toolkit script to reset your keg volume available to 100%.
```bash
🍺  pi@bar[/opt/boozer] >docker exec -ti boozer python /boozer/toolkit.py --reset-tap 1
Loaded config...
	Database file:	/boozer/db.sqlite
----------------------------------------------------
current [Tap 1 ] 0.00 remaining
Are you sure that you reset tapid: 1 (y/n): y
Record: Tap 1 Volume 0
Reset Tap  1
updated! [Tap 1 ] 1.0 remaining
```
protip: another way to reset the tap val to 100% without the toolkit is to add `tap1_reset_database:True` to the taps configuration. NOTE: you will need to remove the line after starting boozer or your tap value will reset every time boozer is restarted.



## Grafana Integration
With a little help from [Telegraf](https://github.com/influxdata/telegraf) (or straight up mqtt with v2) and the Mqtt  message broker, bar stats are viewable in real time with Grafana.

![Grafana is awesome](https://github.com/bgulla/boozer/blob/master/dashboard/bar-dashboard.png?raw=true)

# Home Assistant
Home Assistant is a great tool to pull together all of your home's smart IOT devices into an easy to use, secure tool. Since Boozer can speak mqtt, it can be easily integrated into [Home Assistant](https://home-assistant.io).
![Home Assistant](https://github.com/bgulla/boozer/blob/master/img/hass.png?raw=true)

## Build Pictures
Photos of the bar making process are available [here](https://imgur.com/a/7jnrc).

## FAQs
Most of your questions can probably be answered in the [reddit post](https://www.reddit.com/r/Homebrewing/comments/8lc1wp/introducing_boozer_raspberrypi_controlled/) or the [Hackaday feature](https://hackaday.com/2018/05/28/boozer-tells-the-internet-how-much-you-drink-if-you-want-it-to/).

## Press:
* [Hackaday](https://hackaday.com/2018/05/28/boozer-tells-the-internet-how-much-you-drink-if-you-want-it-to/)
* [Hackster](https://blog.hackster.io/boozer-is-an-open-source-kegerator-monitor-you-can-now-build-with-a-raspberry-pi-5c086e4dfcd4)
* [Adafruit](https://blog.adafruit.com/2018/05/18/raspberry-pi-kegerator-piday-raspberrypi-raspberry_pi/)
* [RaspberryPi.org](https://www.raspberrypi.org/weekly/scouts/)

## Updates
* 5-30-2019: v2 is live
* 5-22-2018: Temperature sensors are now optional.
* 7-1-2018: Toolkit functionality finally documented. Reset tap db values and more. 
* 3-2019: new docker image (boozerbar/boozer). new console logging. more flexible config.

![The Bar That Started It All](https://github.com/bgulla/boozer/blob/master/img/bar.jpg?raw=true)
