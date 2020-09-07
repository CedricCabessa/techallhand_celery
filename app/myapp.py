from celery import Celery
from flask import Flask, redirect, request, url_for, render_template, session

app = Flask(__name__)
app.secret_key = "secret"


def init_celery():
    config = {
        "broker_url": "amqp://guest:guest@rabbitmq:5672/",
        "task_routes": {
            "say_hello": {"queue": "hello_queue"},
            "mine": {"queue": "miner_queue"},
        },
    }

    celery = Celery()
    celery.config_from_object(config)

    return celery


celery = init_celery()


@app.route("/", methods=["GET"])
def home():
    with open("power.txt") as f:
        power = int(f.readline().strip())
    return render_template("home.html", power=power)


@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    celery.send_task(name="say_hello", args=(name,))
    return redirect(url_for("home"))


@app.route("/mine", methods=["POST"])
def mine():
    difficulty = int(request.form["difficulty"])
    session["difficulty"] = difficulty
    celery.send_task(
        name="mine",
        args=(request.form["blockchain"],),
        kwargs={"difficulty": difficulty},
    )
    return redirect(url_for("home"))


@app.route("/power", methods=["POST"])
def update_power():
    power = request.form["power"]
    with open("power.txt", "w") as fp:
        fp.write(f"{power}\n")
    return redirect(url_for("home"))
