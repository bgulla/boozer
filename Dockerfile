FROM resin/rpi-raspbian
MAINTAINER <hey@gulla.xyz>


RUN apt-get update; apt-get install -y python-dev  python-setuptools python-pip python-smbus python-rpi.gpio

COPY ./src/requirements.txt /boozer/
RUN pip install -r /boozer/requirements.txt
COPY ./src/beer_database.py /boozer/
COPY ./db.sqlite /boozer/
COPY ./src/flowmeter.py /boozer/
COPY ./src/twitter_notify.py /boozer/
COPY ./src/bar_mqtt.py /boozer/
COPY ./src/boozer.py /boozer/

WORKDIR /boozer
CMD ["python", "boozer.py"]
