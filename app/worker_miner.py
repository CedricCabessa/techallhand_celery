import time
from celery import Celery


class CryptoException(Exception):
    pass


class MiningException(CryptoException):
    pass


def init_celery():
    config = {"broker_url": "amqp://guest:guest@rabbitmq:5672/"}
    celery = Celery()
    celery.config_from_object(config)

    return celery


celery = init_celery()


@celery.task(name="mine", bind=True)
def mine(self, blockchain, *args, difficulty=1, **kwargs):
    with open("power.txt") as f:
        power = int(f.readline().strip())

    print(">>>>")
    print(f"mine on {blockchain} power={power} difficulty={difficulty}")
    print("<<<<")

    if power < difficulty:
        raise MiningException

    time.sleep(5)
