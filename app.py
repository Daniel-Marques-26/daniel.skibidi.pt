from flask import Flask, render_template, request, session, redirect, url_for
import psycopg


app = Flask(__name__)

app.secret_key = "l)man2/tH6App?av1H"


DB_URL = "postgresql://neondb_owner:npg_skLYJ5R9hIKe@ep-billowing-voice-abofarmr-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
conn = psycopg.connect(DB_URL)


pages_logged = ['home', 'play', 'logout']
pages_not_logged = ['home', 'login', 'register']
pages = 0

def check_login():
    global pages
    if "username" in session:
        pages = pages_logged
    else:
        pages = pages_not_logged

@app.route('/')
@app.route('/home')
def home():

    check_login()

    return render_template("index.html", pages=pages)


@app.route('/login', methods=['POST', 'GET'])
def login():

    check_login()

    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']

        crs = conn.cursor()

        user_info = crs.execute('SELECT "Name" FROM "Users" WHERE "Name"=%s AND "Password"=%s', (username, password)).fetchone()

        if user_info == None:
            msg_add = "That account doesn't exist."
            return render_template("login.html", pages=pages, msg=msg_add)

        else:
            session["username"] = username
            return render_template("play.html", pages=pages)

    if request.method == 'GET':

        return render_template("login.html", pages=pages)


@app.route('/register', methods=['POST', 'GET'])
def register():

    check_login()

    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']
        email = request.form['email']

        crs = conn.cursor()

        user = crs.execute('SELECT "Name" FROM "Users" WHERE "Name"=%s', (username,)).fetchone()

        if user is None:
            crs.execute('INSERT INTO "Users" ("Name", "Password", "Email") VALUES (%s, %s, %s)', (username, password, email))
            crs.close()
            msg_add = "Account created!"
            session['username'] = username
            return render_template("register.html", pages=pages, msg=msg_add)

        elif username == "" or password == "":
            crs.close()
            msg_add = "Are you serious?"
            return render_template("register.html", pages=pages, msg=msg_add)

        crs.close()
        msg_add = "Already existing account!"
        return render_template("register.html", pages=pages, msg=msg_add)

    if request.method == 'GET':

        return render_template("register.html", pages=pages)


@app.route('/play')
def play():

    check_login()

    return render_template("play.html", pages=pages)


@app.route('/logout')
def logout():
    session["username"] = None
    global pages
    return redirect(url_for('home'))


app.run(debug=True, host='0.0.0.0')