FROM resin/rpi-raspbian
MAINTAINER <hey@bgulla.dev>

RUN apt-get update; apt-get install -y python-dev  python-dev python-pip libfreetype6-dev libjpeg-dev build-essential python-setuptools python-pip python-smbus python-rpi.gpio ; apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Nobody likes a root user
RUN mkdir -p /boozer
RUN groupadd -r app &&\
    useradd -r -g app -d /boozer -s /sbin/nologin -c "Docker non-priveleged user" app

ENV HOME=/boozer
ENV APP_HOME=/boozer
#RUN mkdir $APP_HOME

COPY ./src/requirements.txt /boozer/
RUN pip install --upgrade setuptools pip; pip install -r /boozer/requirements.txt
COPY ./db/db.sqlite /boozer/
COPY ./src /boozer
RUN chown -R app:app $APP_HOME

#USER app

WORKDIR /boozer
CMD ["python", "boozer.py"]
