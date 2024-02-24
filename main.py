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


# from typing import Union

# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
