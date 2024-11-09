from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from register_user import register_user
from is_eid_registered import is_eid_registered
from login_user import login_user
import sqlite3  # Database for storing user info
import os

load_dotenv()

# Database setup (replace with a more robust system in production)
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        eID_hash TEXT UNIQUE, 
        salt BLOB, 
        username TEXT PRIMARY KEY, 
        password_hash TEXT
    )
""")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if 'username' in session:
        return redirect(url_for('home'))
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate user
        if login_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        message = "Wrong password or username!"
    return render_template('index.html', message=message)   

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        eid = request.form['eID']
        username = request.form['username']
        password = request.form['password']
        if is_eid_registered(eid):
            message = "Account with this eID is already registered!"
            return render_template('register.html', message=message)
        try:
            register_user(eid, username, password)
            session['username'] = username
            return redirect(url_for('home'))
        except Exception as e:
            message = "Username already taken!"
    return render_template('register.html', message=message)

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate user
        if login_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        message = "Wrong password or username!"
    return render_template('login.html', message=message)
"""
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
