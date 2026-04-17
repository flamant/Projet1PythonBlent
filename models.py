from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basic_store.db'
db = SQLAlchemy(app)





# Définition des modèles
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return 'Product id={0}, name={1}, description={2}, price={3}, stock={4}'.format(self.id, self.name, self.description, self.price, self.stock)

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    
    # Relation avec les éléments du panier
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    user = db.relationship('User', backref='carts')
    
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
    
    def __repr__(self):
        return f'<CartItem {self.id}, Product: {self.product_id}, Qty: {self.quantity}>'


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    statut = db.Column(db.String(20), nullable=False)
    client = db.Column(db.Boolean, unique=False, default=False)
    administrator = db.Column(db.Boolean, unique=False, default=False)


    
    def __repr__(self):
        return 'id={0}, password={1}, statut={2}, client={3}, administrator={4}'.format(self.id, self.password, self.statut, self.client, self.administrator)

with app.app_context():
    db.create_all()  # crée les tables


def add_sample_products_and_add_admin():
    # Créer quelques produits
    products = [
        Product(id='prod001', name='Azus TUF F15', description='PC Portable Gamer', price=899, stock=10),
        Product(id='prod002', name='UGreen Souris sans fil', description='Souris ergonomique', price=49.99, stock=20),
        Product(id='prod003', name='Logitech Clavier mécanique', description='Clavier pour gaming', price=129, stock=15)
    ]

        # Merge évite les doublons si le script est relancé
    for product in products:
        db.session.merge(product)
    
    # Commit pour sauvegarder les changements dans la base de données
    db.session.commit()
    print("Produits ajoutés avec succès!")

    users = [
        User(id='admin@login.fr', password='admin', statut='administrateur',client=False, administrator=True)
    ]

        # Merge évite les doublons si le script est relancé
    for user in users:
        db.session.merge(user)
    
    # Commit pour sauvegarder les changements dans la base de données
    db.session.commit()
    print("administrator ajouté avec succès!")

def read_products():
    # Récupérer tous les produits
    all_products = db.session.query(Product).all()
    # Ajouter à la session
    db.session.add_all(all_products)
    db.session.commit()
    print("\nTous les produits:")
    for product in all_products:
        print(product)

def get_list_of_users():
    # Récupérer tous les utilisateur
    all_users = db.session.query(User).all()
    print("\nTous les utilisateurs:")
    for user in all_users:
        print(user)    


def read_specific_product(product_id):
    # Récupérer un produit spécifique
    specific_product = db.session.query(Product).filter_by(id=product_id).first()
    # Ajouter à la session
    db.session.add(specific_product)
    db.session.commit()
    print("\nProduit spécifique:")
    print(specific_product)
    
def create_product(product):
    if product.__class__.__name__ == 'Product':
        new_product = db.session.query(Product).filter_by(id=product.id).first()
        if new_product is None:
            try:
                new_product = Product(id=product.id, name=product.name, description=product.description, price=product.price, stock=product.stock)
            except ValueError:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
            if new_product.__class__.__name__ == 'Product':
                db.session.merge(new_product)
                db.session.commit()
                print("Produit créé par un administrateur. ")
            else:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
        else:
            raise ValueError("Le produit est déjà créé.")
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")


def update_product(product):
    # Récupérer le produit à mettre à jour
    old_product = db.session.query(Product).filter_by(id=product.id).first()
    # Ajouter à la session
    db.session.add(old_product)
    db.session.commit()
    if old_product:
        # Mettre à jour les attributs
        old_product.name = product.name
        old_product.description = product.description
        old_product.price = product.price
        old_product.stock = product.stock
        
        # Commit pour sauvegarder les changements
        db.session.commit()
        print("\nProduit mis à jour:")
        print(old_product)
    else:
        print("\nProduit non trouvé!")






def delete_product(product_id):
    print("ca passe4")
    # Récupérer le produit à supprimer
    product = db.session.query(Product).filter_by(id=product_id).first()
    # Ajouter à la session
    db.session.add(product)
    db.session.commit()
    if product:
        print("ca passe5")
        # Supprimer le produit
        db.session.delete(product)
        
        # Commit pour sauvegarder les changements
        db.session.commit()
        print("\nProduit avec id=" + product_id + "supprimé!")
    else:
        print("\nProduit non trouvé!")

def create_user(user):
    if user.__class__.__name__ == 'User':
        if len(user.id) > 0 and len(user.password) > 0:
            if (user.client and not user.administrator) or (user.administrator and not user.client):
                try:
                    db.session.query(User).filter_by(id=user.id).one()
                    raise ValueError("L'utilisateur existe déjà en base de donnée.")
                except NoResultFound as e:
                    typeDeCompte = 'client' if user.client else 'administrateur'
                    if user.administrator and user.statut == 'client':
                        raise ValueError("Un client ne peut pas créer un compte administrateur.")
                    print("Creation d'un nouveau compte ",typeDeCompte)
                    print("id=",user.id)
                    # Ajouter à la session
                    db.session.add(user)
                    db.session.commit()
            else:
                raise ValueError("Soit l'utilisateur est client, soit il est administrateur.")
        else:
            raise ValueError("L'identifiant et le mot de passe doivent être renseigné.")
    else:
        raise ValueError("L'utilisateur n'est pas valide.")

def authenticate(id, password):  
    try: 
        db.session.query(User).filter_by(id=id, password=password).one()    
        return True 
    except NoResultFound: 
        print("Cet utilisateur n'existe pas en base.") 
        return False

with app.app_context():
    add_sample_products_and_add_admin()


#print("\nProduits après opérations:")
#for product in session.query(Product).all():
#    print(product)

#session.close()
