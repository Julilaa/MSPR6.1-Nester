from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, send_file
import json
import os

app = Flask(__name__)  # Création d'une instance de l'application Flask.

# Stockage en mémoire des résultats des scans réseau. Les scans sont stockés dans une liste en mémoire pour un accès rapide.
scans = []

# Dictionnaire contenant les utilisateurs autorisés et leurs mots de passe. Utilisé pour l'authentification.
AUTHORIZED_USERS = {'admin': 'adminpassword'}

@app.route('/login', methods=['GET', 'POST'])  # Définit la route pour la page de connexion.
def login():
    # Traitement des requêtes POST pour la connexion utilisateur.
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Vérifie si les identifiants fournis correspondent à un utilisateur autorisé.
        if username in AUTHORIZED_USERS and password == AUTHORIZED_USERS[username]:
            # Création d'une réponse qui redirige l'utilisateur vers la page des scans après une connexion réussie.
            response = make_response(redirect(url_for('get_scans')))
            # Stocke le nom d'utilisateur dans un cookie pour maintenir la session.
            response.set_cookie('username', username)
            return response
        else:
            # Retourne un message d'erreur en cas d'échec de la connexion.
            return "Échec de la connexion. Veuillez réessayer."
    # Affiche la page de connexion pour les requêtes GET.
    return render_template('login.html')

@app.route('/logout')  # Définit la route pour la déconnexion.
def logout():
    # Crée une réponse qui redirige vers la page de connexion.
    response = make_response(redirect(url_for('login')))
    # Supprime le cookie de l'utilisateur pour terminer la session.
    response.set_cookie('username', '', expires=0)
    return response

def is_logged_in():
    # Vérifie si l'utilisateur actuel est connecté en recherchant son cookie.
    username = request.cookies.get('username')
    return username in AUTHORIZED_USERS

@app.route('/scan', methods=['POST'])  # Définit la route pour recevoir les données de scan.
def receive_scan():
    data = request.json  # Récupère les données envoyées en JSON.
    scans.append(data)  # Ajoute les données de scan à la liste `scans`.
    return jsonify({'message': 'Scan reçu avec succès'}), 201  # Retourne une confirmation.

@app.route('/scans', methods=['GET'])  # Définit la route pour afficher les scans enregistrés.
def get_scans():
    if not is_logged_in():
        # Redirige vers la page de connexion si l'utilisateur n'est pas connecté.
        return redirect(url_for('login'))
    # Affiche la page contenant les résultats des scans.
    return render_template('scans.html', scans=scans)

@app.route('/download-json', methods=['GET'])  # Définit la route pour télécharger les scans en format JSON.
def download_json():
    data = scans  # Utilise les scans stockés en mémoire.
    json_file = "scans.json"  # Nom du fichier JSON.

    temp_path = os.path.join('temp', json_file)  # Définit le chemin temporaire pour le fichier JSON.
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)  # Crée le dossier 'temp' si nécessaire.

    with open(temp_path, 'w') as f:  # Ouvre le fichier en écriture.
        json.dump(data, f, indent=4)  # Écrit les données des scans dans le fichier JSON.

    return send_file(temp_path, as_attachment=True, download_name=json_file)  # Envoie le fichier JSON au client.

if __name__ == '__main__':
    app.run(debug=True)  # Lance l'application en mode debug.

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)