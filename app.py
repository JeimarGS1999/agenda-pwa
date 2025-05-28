
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
import json
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Cambiar por una clave más segura

DATA_FILE = 'data.json'
USERS_FILE = 'users.json'

# Crear archivos si no existen
for file in [DATA_FILE, USERS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return 'Usuario o contraseña incorrectos', 403
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        if username in users:
            return 'Usuario ya existe', 409
        users[username] = password
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/api/notes', methods=['GET', 'POST'])
def notes():
    if 'username' not in session:
        return jsonify({'error': 'No autenticado'}), 401

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    username = session['username']
    if username not in data:
        data[username] = {}

    if request.method == 'POST':
        note = request.json
        key = f"{note['day']}_{note['hour']}"
        data[username][key] = note['text']
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)
        return jsonify({'status': 'saved'})

    return jsonify(data[username])

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

if __name__ == '__main__':
    app.run(debug=True)
