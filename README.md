# boozer - Automated Raspberry-Pi powered Kegerator

## Features

[Photo Gallery]()

## Hardware
The following hardware was used in the inital build of boozer but not necessarily required.
 * [Raspberry Pi 3+](https://www.adafruit.com/product/3055)
 * [Flow Sensors (x4)](https://www.adafruit.com/product/828)
   * [1/2 to 1/4 Adapter (x8)](https://www.amazon.com/gp/product/B00AB5X28G)
 * [ScrollPhat LED Display](https://shop.pimoroni.com/products/scroll-phat)
 
 

## Running in Docker
```bash
docker run --rm  -d --name="boozer" \
    --privileged \
    -v <config.ini>:/boozer/config.ini \
    -v <db.sqlite>:/boozer/db.sqlite \
    -t bgulla/boozer
```

## Twitter Alerts
After creating a development application form at [https://apps.twitter.com/](https://apps.twitter.com), Boozer can tweet out whenever a new pour event is detected. See example at [ibuiltabar](https://twitter.com/ibuiltabar).

[Twitter Alerts](https://github.com/bgulla/boozer/blob/master/img/twitter.jpg?raw=true)

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
With a little help from [Telegraf](https://github.com/influxdata/telegraf) and the Mqtt message broker, you bar stats are viewable in real time with Grafana.

![Grafana is awesome](https://github.com/bgulla/boozer/blob/master/dashboard/bar-dashboard.png?raw=true)

