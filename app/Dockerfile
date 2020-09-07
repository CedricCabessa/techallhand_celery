FROM ubuntu:20.04

RUN apt update && \
  apt install -y python3-pip && \
  pip3 install flask celery supervisor

COPY . /app
WORKDIR /app
CMD supervisord -c /app/supervisord.conf
