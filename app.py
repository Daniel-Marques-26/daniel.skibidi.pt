from flask import Flask, render_template, request


app = Flask(__name__)


usuarios = []

pages = ['home', 'login', 'register', 'play']

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", pages=pages)


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html", pages=pages)


@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']

        for u in usuarios:

            if u[0] == username and u[1] == password:
                msg_add = "Already existing account!"
                return render_template("register.html", pages=pages, msg=msg_add)

        if username == "" or password == "":
            msg_add = "Are you serious?"
            return render_template("register.html", pages=pages, msg=msg_add)

        msg_add = "Account created!"
        usuarios.append((username, password))

        return render_template("register.html", pages=pages, msg=msg_add)

    if request.method == 'GET':

        return render_template("register.html", pages=pages)


@app.route('/play')
def play():
    return render_template("play.html", pages=pages)


app.run(debug=True, host='0.0.0.0')