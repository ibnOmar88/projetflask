from flask import Flask
# import sqlite3
from flask_sqlalchemy import SQLAlchemy
# from waitress import serve


app= Flask(__name__)




# configuration

app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key="secret_key"


database=SQLAlchemy(app)



# definition model


inscriptions=database.Table('inscriptions',
                           database.Column('user_id', database.Integer, database.ForeignKey('Users.id')),
                           database.Column('cours_id', database.Integer, database.ForeignKey('cours.id'))
                           )

class User(database.Model):
    __tablename__="Users"
    id= database.Column(database.Integer , primary_key=True, autoincrement=True)
    nom=database.Column(database.String(50), nullable=False)
    email=database.Column(database.String(100), nullable=False)
    password= database.Column(database.String(100), nullable=True)
    # relation one to one 
    carteIdentite=database.relationship('CarteIdentite', backref='Proprietaire', uselist=False)
    # relation one to many
    articles=database.relationship('Article', backref='Auteur')
    # relation many to many
    matiere = database.relationship('Cours', secondary=inscriptions, backref='etudiants')


class CarteIdentite(database.Model):
    __tablename__="cartes"
    id= database.Column(database.Integer , primary_key=True, autoincrement=True)
    NumeroID=database.Column(database.String(100))
    user_id=database.Column(database.Integer, database.ForeignKey('Users.id'), unique=True)



class Article(database.Model):
    id= database.Column(database.Integer , primary_key=True, autoincrement=True)
    titre= database.Column(database.String(50))
    contenu= database.Column(database.Text)
    user_id= database.Column(database.Integer, database.ForeignKey('Users.id'))


class Cours(database.Model):
    id= database.Column(database.Integer , primary_key=True, autoincrement=True)
    libelle_cours=database.Column(database.String(255))
