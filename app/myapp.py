from celery import Celery
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


def init_celery():
    config = {
        "broker_url": "amqp://guest:guest@rabbitmq:5672/",
        "task_routes": {
            "say_hello": {"queue": "hello_queue"},
        },
    }

    celery = Celery()
    celery.config_from_object(config)

    return celery


celery = init_celery()


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/hello", methods=["POST"])
def hello():
    celery.send_task(name="say_hello")
    return redirect(url_for("home"))
