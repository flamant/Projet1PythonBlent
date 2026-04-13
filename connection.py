import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from models import create_user, authenticate, User
from models import app


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"


@app.route('/', methods=["GET"])
def index():
    return jsonify(
        {
            "message": "API en ligne",
            "endpoints": ["/api/auth/register (POST)", "/api/auth/login (POST)", "/health (GET)"]
        }
    ), 200


@app.route('/health', methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route('/api/auth/register', methods=["POST"])
def register_utilisateur():
    body = request.get_json()
    id = body.get("id", "")
    statutDuDemandeur = body.get("statut")
    creerClient = body.get("client")
    creerAdministrateur = body.get("administrator")
    typeDeCompte = 'le client' if statutDuDemandeur == "client" else "l'administrateur"
    password = request.headers.get("password", "0")
    create_user(User(id=id, password=password, statut=statutDuDemandeur, client=creerClient, administrator=creerAdministrateur))
    return jsonify({"message": f"Compte cree pour {typeDeCompte} id={id}"}), 201



@app.route('/api/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    id = body.get("id", "")
    statut = body.get("statut")
    typeDeCompte = 'le client' if statut == "client" else "l'administrateur"
    password = request.headers.get("password", "0")
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