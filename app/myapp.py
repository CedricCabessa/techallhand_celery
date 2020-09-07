import time
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/hello", methods=["POST"])
def hello():
    time.sleep(5)
    print("hello")
    return redirect(url_for("home"))
