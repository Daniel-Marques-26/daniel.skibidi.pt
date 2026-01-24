from flask import Flask, render_template


app = Flask(__name__)


pages = ['home', 'login', 'register', 'play']

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", pages=pages)


@app.route('/login')
def login():
    return render_template("login.html", pages=pages)


@app.route('/register')
def register():
    return render_template("register.html", pages=pages)


@app.route('/play')
def play():
    return render_template("play.html", pages=pages)


app.run(debug=True, host='0.0.0.0')