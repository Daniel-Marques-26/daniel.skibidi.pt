from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return "home"


@app.route('/login')
def login():
    return "login"


@app.route('/register')
def register():
    return "register"


@app.route('/play')
def play():
    return "play"


app.run(debug=True, host='0.0.0.0')