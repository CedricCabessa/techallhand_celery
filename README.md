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


## Add some celery

In the flask app, we create a celery object. We need to specify a "broker_url",
here rabbitmq.

We also need to create a mapping between task and route. I defined a `say_hello`
task that will be route to the `hello_queue` queue

We configure a new worker in supervisord to manage those task. -Q say on which
queue the worker listen.

We implement the worker, it uses a celery object as well (here there is no need
for `task_routes` as this worker do not send tasks.)

The decorator have `bind=True` as parameter, this make the first parameter of
the function be the current task (here we are not in a class!)

We can click on the button, and we see the webpage is more responsive. The
"hello" log is in a celery context.

On interesting thing is the rabbitmq management interface http://localhost:15672

We see the queue automatically created.

When we create a lot of request, we can see them pile up in the queue.

What happen if the worker stop?

```
docker-compose exec app supervisorctl stop worker_hello
```

We see only flask log. Task pile up in queue

```
docker-compose exec app supervisorctl start worker_hello
```

Task are proceed

## Beware of signature

We just add an argument in our task ... and it fails.

Celery use a RPC pattern, so we need to take care of signature.

This is important when producer and consumer run on different machines and have
different life cycle.

## Future proof signature

Write function that can accept any kind of data without crashing
