import jwt
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from models import create_user, authenticate, User, read_products, Product, read_specific_product, get_list_of_users, create_product, update_product, delete_product
from models import app


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

def decode_token(token):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms="HS256"
    )

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
                "user": id,
                "role": "administrateur"
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        data = {"token": token,
        "message": token + "pour " + typeDeCompte + "id=" + id}
        return jsonify(data),200
    else:
        return jsonify({"error": "Identifiant/Mot de passe invalides."}), 401

@app.route('/api/users', methods=["GET"])
def getListOfUsers():
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        get_list_of_users()
        return {"message": "Ok !"}, 200
    else:
        return {"error": "Jeton d'accès invalide ou le role qui fait la demande n'est pas administrateur."}, 401



@app.route('/api/produits', methods=["GET"])
def getProductList():
    token = request.headers.get("token", "0")
    if decode_token(token):
        read_products()
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401

@app.route('/api/produits/<id>', methods=["GET"])
def getSpecificProduct(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        read_specific_product(id)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401


@app.route('/api/produits', methods=["POST"])
def createNewProduct():
    token = request.headers.get("token", "0")
    body = request.get_json()
    id = body.get("id", "")
    name = body.get("name")
    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        create_product(Product(id=id, name=name, description=description, price=price, stock=stock))
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401


@app.route('/api/produits/<id>', methods=["PUT"])
def modifyProduct(id):
    token = request.headers.get("token", "0")
    body = request.get_json()
    name = body.get("name")
    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        print("ca passe3")
        update_product(Product(id=id, name=name, description=description, price=price, stock=stock))
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401

@app.route('/api/produits/<id>', methods=["DELETE"])
def deleteProduct(id):
    print("ca passe1")
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    print("ca passe2")
    if role == "administrateur" and decode_token(token):
        print("ca passe3")
        delete_product(id)
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401


@app.route('/api/commandes', methods=["POST"])
def createNewCommand():
    token = request.headers.get("token", "0")
    body = request.get_json()
    cart_id = body.get("cart_id")
    cart_items = body.get("cart_items")
    item = []
    number_cart_item=0
    for cart_item in cart_items:
        item[number_cart_item]['cart_item_id'] = cart_item['cart_item_id']
        item[number_cart_item]['product_id'] = cart_item['product_id']
        item[number_cart_item]['quantity'] = cart_item['quantity']
        number_cart_item += 1

    try:
        cart = db.session.query(Cart).filter_by(id=cart_id).one()
        return {"error": "This cart already exists."}, 406 
    except NoResultFound:
        print("")
        if decode_token(token):
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("user") 
            i = 0
            while i < number_cart_item:
                try:
                    cart_item[i] = db.session.query(Cart).filter_by(id=item[0]['cart_item_id']).one()
                    return {"error": "This cart_item which id is " + item[0]['cart_item_id'] + " already exists."}, 406 
                except NoResultFound:
                    id_cart_item_max = db.session.query(Cart).filter_by(id=cart_id).one()
                    create_cart_item(CartItem(id=item[i]['cart_item_id'], cart_id=cart_id, product_id=item[i]['product_id'], quantity=item[i]['quantity']))
        else:
            return {"error": "l'utilisateur doit être correctement authentifié."}, 406

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.String(10), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)   

    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        create_product(Product(id=id, name=name, description=description, price=price, stock=stock))
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401