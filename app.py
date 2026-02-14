from flask import Flask, render_template, request, session


app = Flask(__name__)

app.secret_key = "l)man2/tH6App?av1H"


users = []

pages_logged = ['home', 'play', 'logout']
pages_not_logged = ['home', 'login', 'register']
pages = 0

def check_loggin():
    global pages
    if "username" in session:
        pages = pages_logged
    else:
        pages = pages_not_logged

@app.route('/')
@app.route('/home')
def home():

    check_loggin()

    return render_template("index.html", pages=pages)


@app.route('/login', methods=['POST', 'GET'])
def login():

    check_loggin()

    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']

        for u in users:

            if u[0] == username and u[1] == password:
                session["username"] = username
                return render_template("play.html", pages=pages)

    if request.method == 'GET':

        return render_template("login.html", pages=pages)


@app.route('/register', methods=['POST', 'GET'])
def register():

    check_loggin()

    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']

        for u in users:

            if u[0] == username:
                msg_add = "Already existing account!"
                return render_template("register.html", pages=pages, msg=msg_add)

        if username == "" or password == "":
            msg_add = "Are you serious?"
            return render_template("register.html", pages=pages, msg=msg_add)

        msg_add = "Account created!"
        session['username'] = username
        users.append((username, password))

        return render_template("register.html", pages=pages, msg=msg_add)

    if request.method == 'GET':

        return render_template("register.html", pages=pages)


@app.route('/play')
def play():

    check_loggin()

    return render_template("play.html", pages=pages)


app.run(debug=True, host='0.0.0.0')