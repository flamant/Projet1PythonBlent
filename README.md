# Projet1PythonBlent

## Modifications realisees

Cette section resume les corrections et ajouts effectues pour rendre le projet demarrable et testable rapidement.

### 1) Corrections du lancement du serveur Flask

- Correction d'un probleme de contexte Flask dans `models.py`:
  - l'initialisation des donnees (`add_sample_products_and_add_admin`) est maintenant executee dans `app.app_context()`.
- Correction de l'insertion des donnees de base:
  - utilisation de `db.session.merge(...)` pour eviter les doublons si le serveur est relance.
- Installation des dependances manquantes (notamment `PyJWT`) pour permettre le demarrage de l'application.

### 2) Corrections API dans `connection.py`

- Ajout des imports manquants: `User` et `authenticate`.
- Correction de la creation d'utilisateur sur `/api/auth/register`:
  - creation d'un objet `User` valide avec des parametres nommes.
  - ajout d'une reponse JSON explicite avec le code HTTP `201`.
- Correction de la route `/api/auth/login`:
  - correction de la lecture du header `password`.
  - correction de la logique de type de compte pour la generation du token.

### 3) Corrections metier dans `models.py`

- Correction de la validation de type dans `create_user(...)` (`user.__class__.__name__`).
- Correction de la gestion des exceptions SQLAlchemy (`NoResultFound` importe et utilise).
- Correction de `authenticate(...)`:
  - recherche par `id` + `password`.
  - suppression de references a des variables inexistantes.

### 4) Ajout d'endpoints de verification

- Ajout de `GET /`:
  - renvoie un message indiquant que l'API est en ligne et liste les endpoints disponibles.
- Ajout de `GET /health`:
  - renvoie `{"status":"ok"}` pour verifier rapidement l'etat du service.

### 5) Ajout d'un script de test automatique

- Ajout du fichier `test_api.ps1` a la racine du projet.
- Le script teste automatiquement:
  - `GET /`
  - `GET /health`
  - `POST /api/auth/register`
  - `POST /api/auth/login`
- Il affiche des statuts `[OK]` / `[FAIL]` et s'arrete avec un code d'erreur si un test echoue.

## Lancer le projet

Dans le dossier du projet:

```powershell
python -m flask --app connection run
```

Puis, dans un second terminal:

```powershell
powershell -ExecutionPolicy Bypass -File .\test_api.ps1
```