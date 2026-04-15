import requests

req = requests.post("http://127.0.0.1:5000/api/auth/register", headers={"password": "antoine"}, 
json={
    'id': "flamant@club-internet.fr",
    'statut': 'client',
    'client': True,
    'administrator':False
})
print(req.status_code)

req = requests.post("http://127.0.0.1:5000/api/auth/login", headers={"password": "antoine"}, 
json={
    'id': "flamant@club-internet.fr",
    'statut': 'client'
})
print(req.status_code)

token = req.json().get("token")
print(token)

req = requests.get("http://127.0.0.1:5000/api/produits", headers={"token": token})
print(req.status_code)

req = requests.get("http://127.0.0.1:5000/api/produits/prod001", headers={"token": token})
print(req.status_code)

req = requests.post("http://127.0.0.1:5000/api/produits", headers={"token": token},
json={
    'id': "prod004",
    'name': 'souris avec fil S1',
    'description': 'ancien materiel',
    'price':20.5,
    'stock': 30
})
print(req.status_code)

