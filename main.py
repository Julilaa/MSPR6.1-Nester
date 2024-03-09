from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response

app = Flask(__name__)

# Stockage en mémoire des résultats des scans réseau
scans = []

# Dictionnaire d'utilisateurs autorisés
AUTHORIZED_USERS = {'admin': 'adminpassword'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in AUTHORIZED_USERS and password == AUTHORIZED_USERS[username]:
            response = make_response(redirect(url_for('get_scans')))
            response.set_cookie('username', username)
            return response
        else:
            return "Échec de la connexion. Veuillez réessayer."
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('username', '', expires=0)
    return response

def is_logged_in():
    username = request.cookies.get('username')
    return username in AUTHORIZED_USERS

@app.route('/scan', methods=['POST'])
def receive_scan():
    data = request.json
    scans.append(data)
    return jsonify({'message': 'Scan reçu avec succès'}), 201

@app.route('/scans', methods=['GET'])
def get_scans():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('scans.html', scans=scans)

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)