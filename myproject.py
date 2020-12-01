from flask import Flask, render_template, request, session
from flask_session import Session
from helpers import draw_fft_test
import json
from datetime import datetime
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("freq") is None:
        session["freq"] = ''
    if request.method == "POST":
        session["freq"] = request.form.get("freqs")
        session["threshold"] = int(request.form.get("threshold"))
        if session["threshold"] == None:
            session["threshold"] = 50
        session["noise"] = int(request.form.get("noise"))
        if session["noise"] == None:
            session["noise"] = 2
    if session["freq"]:
        all_freqs = list(map(float, session["freq"].split(',')))
        image_name = draw_fft_test(all_freqs, session["threshold"], session["noise"])+'.png'
    else:
        image_name = 'none'
    return render_template("index.html", freq=session["freq"], image_name=image_name)


@app.route("/kursach")
def table():
    return render_template('kursach.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
