from flask import Flask, render_template, request, session, redirect, url_for
import psycopg


app = Flask(__name__)

app.secret_key = "l)man2/tH6App?av1H"


DB_URL = "postgresql://neondb_owner:npg_skLYJ5R9hIKe@ep-billowing-voice-abofarmr-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
conn = psycopg.connect(DB_URL)


pages_logged = ['home', 'play', 'chat', 'logout']
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

        email = request.form['email']
        password = request.form['password']

        crs = conn.cursor()

        user_info = crs.execute('SELECT "Email" FROM "Users" WHERE "Email"=%s AND "Password"=%s', (email, password)).fetchone()

        if user_info == None:
            msg_add = "That account doesn't exist."
            return render_template("login.html", pages=pages, msg=msg_add)

        else:
            print(crs.execute('SELECT "Name" FROM "Users" WHERE "Email"=%s', (email,)).fetchone())
            session["username"] = crs.execute('SELECT "Name" FROM "Users" WHERE "Email"=%s', (email,)).fetchone()[0]
            return redirect(url_for("home"))

    if request.method == 'GET':

        return render_template("login.html", pages=pages)


@app.route('/register', methods=['POST', 'GET'])
def register():

    check_login()

    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']

        crs = conn.cursor()

        user = crs.execute('SELECT "Name" FROM "Users" WHERE "Name"=%s', (username,)).fetchone()

        if user is None and password == password2:
            if username == "" or password == "" or email == "":
                crs.close()
                msg_add = "Are you serious?"
                return render_template("register.html", pages=pages, msg=msg_add)
            crs.execute('INSERT INTO "Users" ("Name", "Password", "Email") VALUES (%s, %s, %s)', (username, password, email))
            conn.commit()
            crs.close()
            msg_add = "Account created!"
            session['username'] = username
            return render_template("register.html", pages=pages, msg=msg_add)

        crs.close()
        msg_add = "Already existing account!"
        return render_template("register.html", pages=pages, msg=msg_add)

    if request.method == 'GET':

        return render_template("register.html", pages=pages)


@app.route('/play')
def play():

    check_login()

    return render_template("game.html", pages=pages)


@app.route('/chat')
def chat():

    return render_template("chat.html", pages=pages, username=session["username"])


@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


app.run(debug=True, host='0.0.0.0')