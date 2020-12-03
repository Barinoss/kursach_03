from flask import Flask, render_template, request, session
from flask_session import Session
from helpers import draw_fft_test, draw_fft

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/kursach", methods=["GET", "POST"])
def kursach():
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
        try:
            all_freqs = list(map(float, session["freq"].split(',')))
        except:
            all_freqs = [1, 2, 3]
        image_name = draw_fft_test(all_freqs, session["threshold"], session["noise"])+'.png'
    else:
        image_name = 'none'
    return render_template("kursach.html", freq=session["freq"], image_name=image_name)


@app.route("/kursach_2", methods=["GET", "POST"])
def kursach_2():
    if session.get("signal") is None:
        session["signal"] = ''
    if request.method == "POST":
        session["signal"] = request.form.get("signal")
        session["threshold"] = int(request.form.get("threshold"))
        if session["threshold"] == None:
            session["threshold"] = 50
    try:
        a = str(session["signal"])
        b = a[1:-1].replace(' ', '').split(',')
        all_freqs = list(map(float, b))
    except:
        all_freqs = [1, 2, 3]
    image_name, signal2 = draw_fft(all_freqs, session["threshold"])
    image_name += '.png'
    return render_template("kursach_2.html", image_name=image_name, signal2=signal2)

@app.route("/")
def index():
    return render_template("layout.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
