import requests

print("register (admin@login.fr, admin) as administrator.")
print("--------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/register", headers={"password": "admin"}, 
json={
    'id': "admin@login.fr",
    'statut': 'client',
    'client': False,
    'administrator':True
})
print("request status is "+ str(req.status_code))


print("connect as (admin@login.fr,admin) (administrator) and generate token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login", headers={"password": "admin"}, 
json={
    'id': "admin@login.fr",
    'statut': 'client'
})
print("request status is "+ str(req.status_code))

token = req.json().get("token")
print("token is:"+ token)

print("get list of users.")
print("------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("request status is "+ str(req.status_code))

print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))

print("get product prod001")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits/prod001", headers={"token": token})
print("request status is "+ str(req.status_code))

print("create a new product ")
print("---------------------")
req = requests.post("http://127.0.0.1:5000/api/produits", headers={"token": token},
json={
    'id': "prod004",
    'name': 'souris avec fil S1',
    'description': 'ancien materiel',
    'price':20.5,
    'stock': 30
})
print("request status is "+ str(req.status_code))

print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))


print("modify a product ")
print("-----------------")
req = requests.put("http://127.0.0.1:5000/api/produits/prod004", headers={"token": token},
json={
    'id': "prod004",
    'name': 'souris avec fil S1 deuxieme version',
    'description': 'ancien materiel deuxieme version',
    'price':24,
    'stock': 40
})
print("request status is "+ str(req.status_code))

print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))

print("delete a product ")
print("-----------------")
req = requests.delete("http://127.0.0.1:5000/api/produits/prod004", headers={"token": token})
print("request status is "+ str(req.status_code))

print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))


print("create a new command ")
print("---------------------")
req = requests.post("http://127.0.0.1:5000/api/commandes", headers={"token": token},
json={
    'user_id': 'flamant@club-internet.fr',
    'cart_id': 'cart001'
    'cart_items' [
        {
            'cart_item_id': 'cartItem001',
            'product_id': 'prod001',
            'quantity': 10
        },
        {
            'cart_item_id': 'cartItem002',
            'product_id': 'prod002',
            'quantity': 20           
        },
        {
            'cart_item_id': 'cartItem003',
            'product_id': 'prod003',
            'quantity': 30
        }
    ]
})
print("request status is "+ str(req.status_code))


class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec les éléments du panier
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cart {self.id}>'

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.String(10), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    # Relation avec le produit
    product = db.relationship('Product', backref='cart_items')