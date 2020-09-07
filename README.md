# Celery introduction

Tech All Hands

Sept 8th 2020

## Intro

[Celery](/en/stable/getting-started/introduction.html) is a distributed task
queue library written in python.

It can use various backend, the most common is rabbitmq.

As per documentation "Task queues are used as a mechanism to distribute work
across threads or machines."

It is used to offload a long running task from a web application (front or api).

Celery is quiet complex and the documentation is not so easy to grasp.

This demo aim to show some basic feature of the library.

You need to explore each commit in the history to follow the demo.

## A simple flask app

We have a simple flask app running in a docker.

For now, we don't use celery.

The app is lauched via [supervisord](http://supervisord.org/), it's a process
supervisor, very useful with docker, as you only need to launch supervisord
and it manages as many subprocess you want via a configuration file.

Inside the docker, you can use `supervisorctl` to restart / stop any process
managed by supervisord. (Actually you can even export the supervisord unix
socket to manage process outside docker). For extra fun, there is a rpc
interface usable via python.

The app show a button that POST on a route that do some long running work (here
a very interesting call to `sleep`).

It's not something we want to do, the page is frozen (see spinner) and the
webserver is stuck processing this request.

