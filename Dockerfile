FROM resin/rpi-raspbian
MAINTAINER <blgulla@ncsu.edu>


RUN apt-get update; apt-get install -y python-dev  python-setuptools python-pip python-smbus python-rpi.gpio

COPY ./src/requirements.txt /boozer/
RUN pip install -r /boozer/requirements.txt
COPY ./src/beer_database.py /boozer/
COPY ./db.sqlite /boozer/
COPY ./src/mqtt_updater.py /boozer/
COPY ./src/flowmeter.py /boozer/
COPY ./src/bartwitter.py /boozer/
COPY ./src/bar_mqtt.py /boozer/
COPY ./src/app.py /boozer/


CMD ["python", "/boozer/app.py]
