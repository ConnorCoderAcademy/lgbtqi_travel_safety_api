import json 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import psycopg2 
import os

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    LGBT_legal_protections = db.Column(db.Boolean)
    population = db.Column(db.Integer,)
    GDP = db.Column(db.BigInteger)
    HDI = db.Column(db.Numeric(10, 3))
    safety_rating = db.Column(db.Float)
    tourism_rating = db.Column(db.Float)
    overall_rating = db.Column(db.Float)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

class City(db.Model):
    __tablename__ = 'cities'
    city_id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    safety_rating = db.Column(db.Float, nullable=False)
    tourism_rating = db.Column(db.Float, nullable=False)
    overall_rating = db.Column(db.Float, nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    safety_rating = db.Column(db.Float, nullable=False)
    tourism_rating = db.Column(db.Float, nullable=False)
    overall_rating = db.Column(db.Float, nullable=False)
