# boozer - Automated Raspberry-Pi Powered Kegerator

![The Bar That Started It All](https://github.com/bgulla/boozer/blob/master/img/bar.jpg?raw=true)
## Features
Kegerator monitoring/volume tracking tool writting in Python. 
 * Track the remaining beer volume of your kegs! Flow sensors keep a running log of your remaining beer volume, using SQLITE.
 * [Twitter](https://twitter.com/ibuiltabar) functionality. Sharing is caring.
 * Temperature Monitoring. [via sensors2json microservice](https://github.com/bgulla/sensor2json)
 
[Photo Gallery](https://imgur.com/a/7jnrc)

## Hardware
The following hardware was used in the inital build of boozer but not necessarily required.
 * [Raspberry Pi 3+](https://www.adafruit.com/product/3055)
 * [Flow Sensors (x4)](https://www.adafruit.com/product/828)
   * [1/2 to 1/4 Adapter (x8)](https://www.amazon.com/gp/product/B00AB5X28G)
 * [ScrollPhat LED Display](https://shop.pimoroni.com/products/scroll-phat)
 * [DS18b20 Waterproof Temperature Sensor](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware)
 
 ![Home Assistant](https://github.com/bgulla/boozer/blob/master/img/breadboard.jpg?raw=true)
 

## Running in Docker
Simplify deployment with Docker. Instructions for installing docker on RaspberryPi's [here](https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/).

```bash
docker run --rm  -d --name="boozer" \
    --privileged \
    -v <config.ini>:/boozer/config.ini \
    -v <db.sqlite>:/boozer/db.sqlite \
    -t bgulla/boozer
```

## Twitter Alerts
After creating a development application form at [https://apps.twitter.com/](https://apps.twitter.com), Boozer can tweet out whenever a new pour event is detected. See example at [ibuiltabar](https://twitter.com/ibuiltabar).

## Configuration Sample
```
[Taps]
tap1_gpio_pin: 24
tap2_gpio_pin: 26 
tap3_gpio_pin: 12 
tap4_gpio_pin: 13
tap1_beer_name: Bud Light
tap2_beer_name: Water
tap3_beer_name: disabled
tap4_beer_name: disabled

[Temperature]
enabled: True
endpoint: http://localhost:8888/chillerf

[Twitter]
enabled: False
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

[Scrollphat]
enabled: True

[Mqtt]
enabled: True
broker: localhost
port: 1883
```

## Grafana Integration
With a little help from [Telegraf](https://github.com/influxdata/telegraf) and the Mqtt message broker, bar stats are viewable in real time with Grafana.

![Grafana is awesome](https://github.com/bgulla/boozer/blob/master/dashboard/bar-dashboard.png?raw=true)

# Home Assistant
Home Assistant is a great tool to pull together all of your home's smart IOT devices into an easy to use, secure tool. Since Boozer can speak mqtt, it can be easily integrated into [Home Assistant](https://home-assistant.io).
![Home Assistant](https://github.com/bgulla/boozer/blob/master/img/hass.png?raw=true)
