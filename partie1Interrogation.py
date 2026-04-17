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
