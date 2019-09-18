from flask import Flask, render_template
from flask_login import LoginManager
from flask import session, redirect, g, request
from functools import wraps
import json

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "jumiabot"

def web_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_login = session.get('session_login', None)
        if not session_login:
            return redirect('/login', 302)
        return f(*args, **kwargs)
    return decorated_function
def file_put_contents(file_name,contents='',mode='w'):
    try:
        with open(file_name, mode) as f:
            f.write(contents)
            return True
    except:
        return False

def file_get_contents(file_name):
    try:
        with open(file_name) as file:
            data = file.read()
            return data.strip()
    except:
        return False

@app.route("/")
@web_login_required
def index():
    products = json.loads(file_get_contents('./products.json'))
    return render_template('dashboard.html',products=products)

@app.route("/logout")
@web_login_required
def logout():
    session_login = session.get('session_login', None)
    if session_login:
        session.pop('session_login')
    return redirect('/login', 302)

@app.route("/login", methods=['GET', 'POST'])
def login():
    context={}
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        if email == 'yacinelaksi2026@gmail.com' and password == 'Yacine123':
            session.permanent = True
            session['session_login'] = "user"
            return redirect('/', 302)
        else:
            context = {"error":"Email or Password Does not match"}
    else:
        session_login = session.get('session_login', None)
        if session_login:
            return redirect('/', 302)
    return render_template('login.html',**context)


if __name__ == '__main__':
    app.run(debug=True, port=8000)