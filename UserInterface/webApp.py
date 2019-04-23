from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/hello/<string:name>/")
def hello(name):
#    return name

    randomNumber = randint(0,10)

    return render_template('test.html',**locals())

if __name__ == "__main__":
    app.run(host='localhost', port=8000)
