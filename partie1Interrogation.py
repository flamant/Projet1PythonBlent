import requests
import settings

print("Inscription d'un nouvel utilisateur (POST /api/auth/register).")
print("--------------------------------------------------------------")

#print("register (admin@login.fr, admin) as administrator.")
#print("--------------------------------------------------")
#req = requests.post("http://127.0.0.1:5000/api/auth/register", headers={"password": "admin"}, 
#json={
#    'id': "admin@login.fr",
#    'statut': 'client',
#    'client': False,
#    'administrator':True
#})
#print("request status is "+ str(req.status_code))

print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connect as (admin@login.fr,admin) (administrator) and generate token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login", headers={"password": "admin"}, 
json={
    'id': "admin@login.fr",
    'statut': 'administrateur'
})
print("request status is "+ str(req.status_code))

token = req.json().get("token")
print("token is:"+ token)

print("get list of users interrogé par un administrateur.")
print("--------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("request status is "+ str(req.status_code))

print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))


print("Récupérer un produit spécifique (GET /api/produits/{id})")
print("get product prod001")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits/prod001", headers={"token": token})
print("request status is "+ str(req.status_code))


print("Créer un nouveau produit (POST /api/produits) - Admin uniquement")
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


print("Modifier un produit existant (PUT /api/produits/{id}) - Admin uniquement")
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


print("Supprimer un produit (DELETE /api/produits/{id}) - Admin uniquement")
print("delete a product ")
print("-----------------")
req = requests.delete("http://127.0.0.1:5000/api/produits/prod004", headers={"token": token})
print("request status is "+ str(req.status_code))

print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))


print("Créer une nouvelle commande (POST /api/commandes) - Admin uniquement")
print("create a new command as administrator")
print("-------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/commandes", headers={"token": token},
json={
    'cart_id': 1,
    'cart_items': [
        {
            'cart_item_id': 1,
            'product_id': 'prod001',
            'quantity': 10
        },
        {
            'cart_item_id': 2,
            'product_id': 'prod002',
            'quantity': 20           
        },
        {
            'cart_item_id': 3,
            'product_id': 'prod003',
            'quantity': 30
        }
    ]
})
print("request status is "+ str(req.status_code))
settings.init() 
#print("json response")
#print(req.json())


print("Récupérer la liste des produits (GET /api/produits)")
print("get list of products.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print("request status is "+ str(req.status_code))

#print("request status is "+ str(req.json()))


print("Récupérer la liste des commandes (GET /api/commandes) - Admin voit tout, client voit ses commandes")
print("get list of carts.")
print("---------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes", headers={"token": token})
print("request status is "+ str(req.status_code))


print("Consulter les lignes d'une commande (GET /api/commandes/{id}/lignes)")
print("get list of cart items.")
print("-----------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes/1/lignes", headers={"token": token})
print("request status is "+ str(req.status_code))

print("Inscription d'un nouvel utilisateur (POST /api/auth/register).")
print("--------------------------------------------------------------")
#print("register (flamant@club-internet.fr, antoine) as client.")
#print("--------------------------------------------------")
#req = requests.post("http://127.0.0.1:5000/api/auth/register", headers={"password": "antoine"}, 
#json={
#    'id': "flamant@club-internet.fr",
#    'statut': 'client',
#    'client': True,
#    'administrator':False
#})
#print("request status is "+ str(req.status_code))


print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connect as (flamant@club-internet.fr,antoine) (client) and generate token.")
print("--------------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login", headers={"password": "antoine"}, 
json={
    'id': "flamant@club-internet.fr",
    'statut': 'client'
})
print("request status is "+ str(req.status_code))
token_client = req.json().get("token")
print("token is:"+ token_client)


print("Créer une nouvelle commande (POST /api/commandes)")
print("create a new command as client")
print("------------------------------")
req = requests.post("http://127.0.0.1:5000/api/commandes", headers={"token": token_client},
json={
    'cart_id': 2,
    'cart_items': [
        {
            'cart_item_id': 4,
            'product_id': 'prod001',
            'quantity': 5
        }
    ]
})
print("request status is "+ str(req.status_code))
settings.init() 
#print("json response")
#print(req.json())


print("Récupérer la liste des commandes (GET /api/commandes) - Admin voit tout, client voit ses commandes")
print("get list of carts as client.")
print("----------------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes", headers={"token": token_client})
print("request status is "+ str(req.status_code))

print("Récupérer la liste des commandes (GET /api/commandes) - Admin voit tout, client voit ses commandes")
print("get list of carts as administrator.")
print("-----------------------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes", headers={"token": token})
print("request status is "+ str(req.status_code))

print("Récupérer une commande spécifique (GET /api/commandes/{id})")
print("Récupérer une commande spécifique (GET /api/commandes/{id}) (client or administrator)")
print("-------------------------------------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes/1", headers={"token": token})
print("request status is "+ str(req.status_code))


print("Modifier le statut d'une commande (de processing a cancelled) (PATCH /api/commandes/{id}) - Admin uniquement")
print("------------------------------------------------------------------------------------------------------------")
req = requests.patch("http://127.0.0.1:5000/api/commandes/1", headers={"token": token},
json={
    'cart_id': 2,
    'cart_items': [
        {
            'cart_item_id': 4,
            'product_id': 'prod001',
            'quantity': 5
        }]})
print("request status is "+ str(req.status_code))


