FROM resin/rpi-raspbian
MAINTAINER <brandon@brandongulla.com>

RUN apt-get update; apt-get install -y python-dev  python-setuptools python-pip python-smbus python-rpi.gpio ; apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Nobody likes a root user
RUN mkdir -p /boozer
RUN groupadd -r app &&\
    useradd -r -g app -d /boozer -s /sbin/nologin -c "Docker image user" app

ENV HOME=/boozer
ENV APP_HOME=/boozer
#RUN mkdir $APP_HOME

COPY ./src/requirements.txt /boozer/
RUN pip install -r /boozer/requirements.txt
COPY ./src/beer_db.py /boozer/
COPY ./db.sqlite /boozer/
COPY ./src/flowmeter.py /boozer/
COPY ./src/twitter_notify.py /boozer/
COPY ./src/bar_mqtt.py /boozer/
COPY ./src/boozer.py /boozer/
COPY ./src/toolkit.py /boozer/

RUN chown -R app:app $APP_HOME

#USER app

WORKDIR /boozer
CMD ["python", "boozer.py"]
