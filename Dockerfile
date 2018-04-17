FROM resin/rpi-raspbian
MAINTAINER <blgulla@ncsu.edu>


RUN apt-get update; apt-get install -y python-dev  python-setuptools python-pip python-smbus python-rpi.gpio

COPY ./requirements.txt /boozer/
RUN pip install -r /boozer/requirements.txt
COPY ./beer_database.py /boozer/
COPY ./db.sqlite /boozer/
COPY ./mqtt_updater.py /boozer/
COPY ./flowmeter.py /boozer/
COPY ./bartwitter.py /boozer/
COPY ./bar_mqtt.py /boozer/
COPY ./app.py /boozer/


CMD ["python", "/boozer/app.py]
