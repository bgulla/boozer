# boozer - Automated Raspberry-Pi powered Kegerator

## Hardware

## Running in Docker
```bash
docker run --rm  -d --name="boozer" \
    --privileged \
    -v <config.ini>:/boozer/config.ini \
    -v <db.sqlite>:/boozer/db.sqlite \
    -t bgulla/boozer
```

# Configuration Sample
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


## Known Issues
 * There is currently no way to reset the tap values without manual sqlite modification or running the beer_database.py file's main method. (warning: this will reset all taps)
