import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

app = Flask(__name__)

@app.route('/api/auth/register', methods=["POST"])
def register_utilisateur():
    body = request.get_json()
    id = body.get("id", "")
    statutDuDemandeur = body.get("statut")
    creerClient = body.get("client")
    creerAdministrateur = body.get("administrator")
    typeDeCompte = 'le client' if user.statut == "client" else "l'administrateur"
    password = request.headers.get("password", "0")
    create_user(User(id, password, statutDuDemandeur, creerClient, creerAdministrateur))



@app.route('/api/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    id = body.get("id", "")
    statut = body.get("statut")
    typeDeCompte = 'le client' if user.client else "l'administrateur"
    password = request.headers.get("Password", "0")
    if authenticate(id, password):
        token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(hours=1),
                "user": statut + id
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        return jsonify({"token": token + "pour " + typeDeCompte + "id=" + id}), 200
    else:
        return jsonify({"error": "Identifiant/Mot de passe invalides."}), 401