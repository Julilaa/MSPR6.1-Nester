from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage en mémoire des résultats des scans réseau
scans = []

@app.route('/scan', methods=['POST'])
def receive_scan():
    data = request.json  # Recevoir les données JSON de la requête POST
    scans.append(data)   # Stocker les données reçues
    return jsonify({'message': 'Scan reçu avec succès'}), 201

@app.route('/scans', methods=['GET'])
def get_scans():
    return jsonify(scans), 200

if __name__ == '__main__':
    app.run(debug=True)

