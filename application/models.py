from db.connection import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String,unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Integer)


class Category(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nProd = db.Column(db.Integer)
    name = db.Column(db.String,unique=True, nullable=False)


class Product(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True, nullable=False)
    Manu_date = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))