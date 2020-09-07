import time
from celery import Celery


def init_celery():
    config = {"broker_url": "amqp://guest:guest@rabbitmq:5672/"}
    celery = Celery()
    celery.config_from_object(config)

    return celery


celery = init_celery()


@celery.task(name="say_hello", bind=True)
def hello(self):
    time.sleep(5)
    print("hello")
