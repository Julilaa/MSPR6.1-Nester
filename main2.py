import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)
AUTHORIZED_USERS = {'admin': 'password'}  # Remplacer par vos propres utilisateurs

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in AUTHORIZED_USERS and password == AUTHORIZED_USERS[username]:
            response = redirect(url_for('results'))
            response.set_cookie('username', username)
            return response
        else:
            return "Login échoué. Veuillez réessayer.", 401
    return render_template('login.html')

@app.route('/results', methods=['GET'])
def results():
    username = request.cookies.get('username')
    if not username or username not in AUTHORIZED_USERS:
        return redirect(url_for('login'))

    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
    results = []
    for file_name in files:
        file_path = os.path.join(data_folder, file_name)
        with open(file_path, 'r') as file:
            results.extend(json.load(file))

    return render_template('results.html', results=results)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'Aucun fichier fourni'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Aucun fichier sélectionné'}), 400
    if file:
        filename = file.filename
        data_folder = os.path.join(os.path.dirname(__file__), 'data')
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        file_path = os.path.join(data_folder, filename)
        file.save(file_path)
        return jsonify({'message': 'Fichier téléchargé avec succès', 'filename': filename}), 201

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('username')
    return response

if __name__ == '__main__':
    app.run(debug=True)
