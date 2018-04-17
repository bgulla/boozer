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
# Grafana Integration


## Known Issues
 * There is currently no way to reset the tap values without manual sqlite modification or running the beer_database.py file's main method. (warning: this will reset all taps)
