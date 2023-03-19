import json 
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import psycopg2 
import os
import click
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import jwt
from werkzeug.security import generate_password_hash
import datetime
import functools

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://connorhay:123456@localhost:5432/lgbtqi_travel_api'

db = SQLAlchemy(app)
ma = Marshmallow(app)


# models

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lgbt_legal_protections = db.Column(db.Boolean, default=False)
    population = db.Column(db.Integer,)
    gdp = db.Column(db.BigInteger)
    hdi = db.Column(db.Numeric(10, 3))
    safety_rating = db.Column(db.Float)
    tourism_rating = db.Column(db.Float)
    overall_rating = db.Column(db.Float)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    safety_rating = db.Column(db.Float, nullable=False)
    tourism_rating = db.Column(db.Float, nullable=False)
    overall_rating = db.Column(db.Float, nullable=False)

#schemas 
class CountrySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "lgbt_legal_protections", "population", "gdp", "hdi", "safety_rating", "tourism_rating", "overall_rating")

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'email', 'password', 'admin')


#multiple countries schema, to handle countries list

#cli 
@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("Database created")

@app.cli.command("drop_db")
def drop_db():
    db.drop_all()
    print("Database dropped.")
      
@app.cli.command("seed_countries")
def seed_countries():
    countries_data = [
        {"id": 1, "name": "Afghanistan", "lgbt_legal_protections": False, "population": 39835428, "gdp": 19900000000, "hdi": 0.511, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 2, "name": "Albania", "lgbt_legal_protections": False, "population": 2845955, "gdp": 15700000000, "hdi": 0.795, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 3, "name": "Algeria", "lgbt_legal_protections": False, "population": 44616626, "gdp": 162800000000, "hdi": 0.759, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 4, "name": "Andorra", "lgbt_legal_protections": False, "population": 78015, "gdp": 2900000000, "hdi": 0.868, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 5, "name": "Angola", "lgbt_legal_protections": False, "population": 33417694, "gdp": 85300000000, "hdi": 0.581, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 6, "name": "Antigua and Barbuda", "lgbt_legal_protections": False, "population": 103050, "gdp": 1700000000, "hdi": 0.778, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 7, "name": "Argentina", "lgbt_legal_protections": False, "population": 45808747, "gdp": 383800000000, "hdi": 0.830, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 8, "name": "Armenia", "lgbt_legal_protections": False, "population": 2968128, "gdp": 14700000000, "hdi": 0.776, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 9, "name": "Australia", "lgbt_legal_protections": True, "population": 25788319, "gdp": 1400000000000, "hdi": 0.944, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 10, "name": "Austria", "lgbt_legal_protections": True, "population": 9015361, "gdp": 487500000000, "hdi": 0.922, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 11, "name": "Azerbaijan", "lgbt_legal_protections": False, "population": 10110116, "gdp": 47500000000, "hdi": 0.769, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 12, "name": "Bahamas", "lgbt_legal_protections": False, "population": 399285, "gdp": 13700000000, "hdi": 0.812, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 13, "name": "Bahrain", "lgbt_legal_protections": False, "population": 1748324, "gdp": 36300000000, "hdi": 0.852, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 14, "name": "Bangladesh", "lgbt_legal_protections": False, "population": 166303498, "gdp": 352200000000, "hdi": 0.632, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 15, "name": "Barbados", "lgbt_legal_protections": False, "population": 287025, "gdp": 5000000000, "hdi": 0.800, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 16, "name": "Belarus", "lgbt_legal_protections": False, "population": 9449323, "gdp": 60200000000, "hdi": 0.808, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 17, "name": "Belgium", "lgbt_legal_protections": False, "population": 11632335, "gdp": 528300000000, "hdi": 0.919, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 18, "name": "Belize", "lgbt_legal_protections": False, "population": 408487, "gdp": 1800000000, "hdi": 0.724, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 19, "name": "Benin", "lgbt_legal_protections": False, "population": 12315244, "gdp": 14400000000, "hdi": 0.545, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 20, "name": "Bhutan", "lgbt_legal_protections": False, "population": 771608, "gdp": 3000000000, "hdi": 0.654, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 21, "name": "Bolivia", "lgbt_legal_protections": False, "population": 11836453, "gdp": 41200000000, "hdi": 0.718, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 22, "name": "Bosnia and Herzegovina", "lgbt_legal_protections": False, "population": 3301000, "gdp": 19200000000, "hdi": 0.780, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 23, "name": "Botswana", "lgbt_legal_protections": False, "population": 2397000, "gdp": 15500000000, "hdi": 0.717, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 24, "name": "Brazil", "lgbt_legal_protections": True, "population": 213993437, "gdp": 1500000000000, "hdi": 0.765, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 25, "name": "Brunei", "lgbt_legal_protections": False, "population": 459500, "gdp": 12600000000, "hdi": 0.856, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 26, "name": "Bulgaria", "lgbt_legal_protections": False, "population": 7000000, "gdp": 66200000000, "hdi": 0.812, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 27, "name": "Burkina Faso", "lgbt_legal_protections": False, "population": 21510084, "gdp": 16800000000, "hdi": 0.452, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 28, "name": "Burundi", "lgbt_legal_protections": False, "population": 11890781, "gdp": 3000000000, "hdi": 0.423, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 29, "name": "Cabo Verde", "lgbt_legal_protections": False, "population": 549935, "gdp": 2000000000, "hdi": 0.737, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 30, "name": "Cambodia", "lgbt_legal_protections": False, "population": 16945587, "gdp": 31500000000, "hdi": 0.611, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 31, "name": "Cameroon", "lgbt_legal_protections": False, "population": 26944000, "gdp": 40500000000, "hdi": 0.563, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 32, "name": "Canada", "lgbt_legal_protections": True, "population": 38005238, "gdp": 1800000000000, "hdi": 0.929, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 33, "name": "Central African Republic", "lgbt_legal_protections": False, "population": 4830000, "gdp": 1900000000, "hdi": 0.382, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 34, "name": "Chad", "lgbt_legal_protections": False, "population": 16535000, "gdp": 13400000000, "hdi": 0.404, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 35, "name": "Chile", "lgbt_legal_protections": True, "population": 19298150, "gdp": 330300000000, "hdi": 0.851, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 36, "name": "China", "lgbt_legal_protections": False, "population": 1444216100, "gdp": 16400000000000, "hdi": 0.761, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 37, "name": "Colombia", "lgbt_legal_protections": True, "population": 50339443, "gdp": 333500000000, "hdi": 0.767, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 38, "name": "Comoros", "lgbt_legal_protections": False, "population": 873724, "gdp": 700000000, "hdi": 0.527, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 39, "name": "Congo, Democratic Republic of the", "lgbt_legal_protections": False, "population": 101780263, "gdp": 40100000000, "hdi": 0.488, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 40, "name": "Congo, Republic of the", "lgbt_legal_protections": False, "population": 5518087, "gdp": 12400000000, "hdi": 0.606, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 41, "name": "Costa Rica", "lgbt_legal_protections": True, "population": 5139776, "gdp": 66800000000, "hdi": 0.830, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 42, "name": "Cote d'Ivoire", "lgbt_legal_protections": False, "population": 27961193, "gdp": 58800000000, "hdi": 0.485, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 43, "name": "Croatia", "lgbt_legal_protections": False, "population": 4087843, "gdp": 62700000000, "hdi": 0.837, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 44, "name": "Cuba", "lgbt_legal_protections": True, "population": 11326616, "gdp": 21600000000, "hdi": 0.778, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 45, "name": "Cyprus", "lgbt_legal_protections": False, "population": 1217800, "gdp": 28300000000, "hdi": 0.869, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 46, "name": "Czech Republic", "lgbt_legal_protections": True, "population": 10724567, "gdp": 268700000000, "hdi": 0.903, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 47, "name": "Denmark", "lgbt_legal_protections": True, "population": 5822763, "gdp": 306900000000, "hdi": 0.940, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 48, "name": "Djibouti", "lgbt_legal_protections": False, "population": 1078373, "gdp": 2200000000, "hdi": 0.498, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 49, "name": "Dominica", "lgbt_legal_protections": False, "population": 71808, "gdp": 500000000, "hdi": 0.717, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 50, "name": "Dominican Republic", "lgbt_legal_protections": False, "population": 10738957, "gdp": 88900000000, "hdi": 0.745, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 51, "name": "Ecuador", "lgbt_legal_protections": True, "population": 17741499, "gdp": 73800000000, "hdi": 0.759, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 52, "name": "Egypt", "lgbt_legal_protections": False, "population": 104258327, "gdp": 303100000000, "hdi": 0.706, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 53, "name": "El Salvador", "lgbt_legal_protections": False, "population": 6486201, "gdp": 25900000000, "hdi": 0.665, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 54, "name": "Equatorial Guinea", "lgbt_legal_protections": False, "population": 1402985, "gdp": 12600000000, "hdi": 0.592, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 55, "name": "Eritrea", "lgbt_legal_protections": False, "population": 3546421, "gdp": 1400000000, "hdi": 0.440, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 56, "name": "Estonia", "lgbt_legal_protections": True, "population": 1317840, "gdp": 32700000000, "hdi": 0.877, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 57, "name": "Eswatini (formerly Swaziland)", "lgbt_legal_protections": False, "population": 1160164, "gdp": 5600000000, "hdi": 0.608, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 58, "name": "Ethiopia", "lgbt_legal_protections": False, "population": 114963583, "gdp": 96500000000, "hdi": 0.470, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 59, "name": "Fiji", "lgbt_legal_protections": False, "population": 896758, "gdp": 5100000000, "hdi": 0.740, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 60, "name": "Finland", "lgbt_legal_protections": True, "population": 5540720, "gdp": 269700000000, "hdi": 0.938, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 61, "name": "France", "lgbt_legal_protections": True, "population": 67614757, "gdp": 2800000000000, "hdi": 0.901, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 62, "name": "Gabon", "lgbt_legal_protections": False, "population": 2225734, "gdp": 11500000000, "hdi": 0.703, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 63, "name": "Gambia", "lgbt_legal_protections": False, "population": 2488578, "gdp": 900000000, "hdi": 0.462, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 64, "name": "Georgia", "lgbt_legal_protections": False, "population": 3714000, "gdp": 17400000000, "hdi": 0.782, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 65, "name": "Germany", "lgbt_legal_protections": True, "population": 83240525, "gdp": 4300000000000, "hdi": 0.939, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 66, "name": "Ghana", "lgbt_legal_protections": False, "population": 31296398, "gdp": 83100000000, "hdi": 0.611, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 67, "name": "Greece", "lgbt_legal_protections": True, "population": 10473455, "gdp": 216800000000, "hdi": 0.888, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 68, "name": "Grenada", "lgbt_legal_protections": False, "population": 112003, "gdp": 1100000000, "hdi": 0.768, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 69, "name": "Guatemala", "lgbt_legal_protections": False, "population": 18232000, "gdp": 80300000000, "hdi": 0.650, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 70, "name": "Guinea", "lgbt_legal_protections": False, "population": 13052679, "gdp": 13100000000, "hdi": 0.464, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 71, "name": "GuineaBissau", "lgbt_legal_protections": False, "population": 1932871, "gdp": 1000000000, "hdi": 0.454, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 72, "name": "Guyana", "lgbt_legal_protections": False, "population": 790326, "gdp": 4100000000, "hdi": 0.640, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 73, "name": "Haiti", "lgbt_legal_protections": False, "population": 11263077, "gdp": 9100000000, "hdi": 0.498, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 74, "name": "Honduras", "lgbt_legal_protections": False, "population": 10183339, "gdp": 27700000000, "hdi": 0.644, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 75, "name": "Hungary", "lgbt_legal_protections": False, "population": 9648921, "gdp": 170300000000, "hdi": 0.854, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 76, "name": "Iceland", "lgbt_legal_protections": True, "population": 339031, "gdp": 19800000000, "hdi": 0.938, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 77, "name": "India", "lgbt_legal_protections": True, "population": 1393409038, "gdp": 3100000000000, "hdi": 0.645, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 78, "name": "Indonesia", "lgbt_legal_protections": False, "population": 273523615, "gdp": 1100000000000, "hdi": 0.718, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 79, "name": "Iran", "lgbt_legal_protections": False, "population": 83992953, "gdp": 630000000000, "hdi": 0.783, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 80, "name": "Iraq", "lgbt_legal_protections": False, "population": 40222493, "gdp": 178200000000, "hdi": 0.654, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 81, "name": "Ireland", "lgbt_legal_protections": True, "population": 4977400, "gdp": 391100000000, "hdi": 0.955, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 82, "name": "Israel", "lgbt_legal_protections": True, "population": 9053300, "gdp": 395200000000, "hdi": 0.919, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 83, "name": "Italy", "lgbt_legal_protections": False, "population": 60340328, "gdp": 2100000000000, "hdi": 0.880, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 84, "name": "Jamaica", "lgbt_legal_protections": False, "population": 2961167, "gdp": 14400000000, "hdi": 0.778, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 85, "name": "Japan", "lgbt_legal_protections": False, "population": 126264931, "gdp": 4900000000000, "hdi": 0.920, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 86, "name": "Jordan", "lgbt_legal_protections": False, "population": 10203140, "gdp": 45300000000, "hdi": 0.732, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 87, "name": "Kazakhstan", "lgbt_legal_protections": False, "population": 19159000, "gdp": 181400000000, "hdi": 0.818, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 88, "name": "Kenya", "lgbt_legal_protections": False, "population": 54542000, "gdp": 101400000000, "hdi": 0.610, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 89, "name": "Kiribati", "lgbt_legal_protections": False, "population": 122000, "gdp": 300000000, "hdi": 0.640, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 90, "name": "Kosovo", "lgbt_legal_protections": False, "population": 1845300, "gdp": 7500000000, "hdi": 0.814, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 91, "name": "Kuwait", "lgbt_legal_protections": False, "population": 4383652, "gdp": 116500000000, "hdi": 0.800, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 92, "name": "Kyrgyzstan", "lgbt_legal_protections": False, "population": 6524195, "gdp": 8500000000, "hdi": 0.699, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 93, "name": "Laos", "lgbt_legal_protections": False, "population": 7262100, "gdp": 19600000000, "hdi": 0.613, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 94, "name": "Latvia", "lgbt_legal_protections": False, "population": 1906100, "gdp": 32100000000, "hdi": 0.847, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 95, "name": "Lebanon", "lgbt_legal_protections": False, "population": 6859408, "gdp": 49600000000, "hdi": 0.780, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 96, "name": "Lesotho", "lgbt_legal_protections": False, "population": 2142249, "gdp": 2600000000, "hdi": 0.519, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 97, "name": "Liberia", "lgbt_legal_protections": False, "population": 5180538, "gdp": 3000000000, "hdi": 0.485, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 98, "name": "Libya", "lgbt_legal_protections": False, "population": 6871292, "gdp": 51600000000, "hdi": 0.724, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 99, "name": "Liechtenstein", "lgbt_legal_protections": False, "population": 38380, "gdp": 6100000000, "hdi": 0.94, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 100, "name": "Lithuania", "lgbt_legal_protections": False, "population": 2722289, "gdp": 56300000000, "hdi": 0.869, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 101, "name": "Luxembourg", "lgbt_legal_protections": True, "population": 634730, "gdp": 74700000000, "hdi": 0.904, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 102, "name": "Madagascar", "lgbt_legal_protections": False, "population": 29126082, "gdp": 14100000000, "hdi": 0.467, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 103, "name": "Malawi", "lgbt_legal_protections": False, "population": 19915316, "gdp": 8800000000, "hdi": 0.485, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 104, "name": "Malaysia", "lgbt_legal_protections": False, "population": 32365999, "gdp": 336000000000, "hdi": 0.820, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 105, "name": "Maldives", "lgbt_legal_protections": False, "population": 540542, "gdp": 5700000000, "hdi": 0.723, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 106, "name": "Mali", "lgbt_legal_protections": False, "population": 20250834, "gdp": 19900000000, "hdi": 0.427, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 107, "name": "Malta", "lgbt_legal_protections": True, "population": 514564, "gdp": 16200000000, "hdi": 0.869, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 108, "name": "Marshall Islands", "lgbt_legal_protections": False, "population": 59190, "gdp": 200000000, "hdi": 0.64, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 109, "name": "Mauritania", "lgbt_legal_protections": False, "population": 4812107, "gdp": 6900000000, "hdi": 0.521, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 110, "name": "Mauritius", "lgbt_legal_protections": False, "population": 1271768, "gdp": 15600000000, "hdi": 0.796, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 111, "name": "Mexico", "lgbt_legal_protections": True, "population": 130222815, "gdp": 1200000000000, "hdi": 0.774, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 112, "name": "Micronesia", "lgbt_legal_protections": False, "population": 116254, "gdp": 400000000, "hdi": 0.628, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 113, "name": "Moldova", "lgbt_legal_protections": False, "population": 2635125, "gdp": 12700000000, "hdi": 0.728, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 114, "name": "Monaco", "lgbt_legal_protections": False, "population": 39244, "gdp": 7300000000, "hdi": 0.956, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 115, "name": "Mongolia", "lgbt_legal_protections": False, "population": 3317786, "gdp": 14600000000, "hdi": 0.744, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 116, "name": "Montenegro", "lgbt_legal_protections": False, "population": 628960, "gdp": 6300000000, "hdi": 0.814, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 117, "name": "Morocco", "lgbt_legal_protections": False, "population": 37291567, "gdp": 124700000000, "hdi": 0.686, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 118, "name": "Mozambique", "lgbt_legal_protections": False, "population": 32077675, "gdp": 16200000000, "hdi": 0.456, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 119, "name": "Myanmar (formerly Burma)", "lgbt_legal_protections": False, "population": 53855735, "gdp": 81800000000, "hdi": 0.584, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 120, "name": "Namibia", "lgbt_legal_protections": False, "population": 2568569, "gdp": 14200000000, "hdi": 0.644, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 121, "name": "Nauru", "lgbt_legal_protections": False, "population": 10860, "gdp": 100000000, "hdi": 0.721, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 122, "name": "Nepal", "lgbt_legal_protections": False, "population": 29996478, "gdp": 31800000000, "hdi": 0.579, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 123, "name": "Netherlands", "lgbt_legal_protections": True, "population": 17173005, "gdp": 1000000000000, "hdi": 0.944, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 124, "name": "New Zealand", "lgbt_legal_protections": True, "population": 4987072, "gdp": 209900000000, "hdi": 0.936, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 125, "name": "Nicaragua", "lgbt_legal_protections": False, "population": 6624554, "gdp": 13700000000, "hdi": 0.658, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 126, "name": "Niger", "lgbt_legal_protections": False, "population": 26495573, "gdp": 7500000000, "hdi": 0.427, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 127, "name": "Nigeria", "lgbt_legal_protections": False, "population": 211400000, "gdp": 504600000000, "hdi": 0.539, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 128, "name": "North Korea", "lgbt_legal_protections": False, "population": 25778816, "gdp": 29000000000, "hdi": 0.766, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 129, "name": "North Macedonia (formerly Macedonia)", "lgbt_legal_protections": False, "population": 2082958, "gdp": 14300000000, "hdi": 0.807, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 130, "name": "Norway", "lgbt_legal_protections": True, "population": 5460823, "gdp": 404900000000, "hdi": 0.957, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 131, "name": "Oman", "lgbt_legal_protections": False, "population": 5106626, "gdp": 71800000000, "hdi": 0.820, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 132, "name": "Pakistan", "lgbt_legal_protections": False, "population": 225200000, "gdp": 278200000000, "hdi": 0.560, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 133, "name": "Palau", "lgbt_legal_protections": False, "population": 17907, "gdp": 300000000, "hdi": 0.767, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 134, "name": "Palestine", "lgbt_legal_protections": False, "population": 5200000, "gdp": 15000000000, "hdi": 0.715, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 135, "name": "Panama", "lgbt_legal_protections": False, "population": 4377098, "gdp": 74900000000, "hdi": 0.820, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 136, "name": "Papua New Guinea", "lgbt_legal_protections": False, "population": 8947027, "gdp": 24300000000, "hdi": 0.555, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 137, "name": "Paraguay", "lgbt_legal_protections": False, "population": 7132538, "gdp": 40200000000, "hdi": 0.720, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 138, "name": "Peru", "lgbt_legal_protections": False, "population": 33421825, "gdp": 226200000000, "hdi": 0.777, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 139, "name": "Philippines", "lgbt_legal_protections": False, "population": 110376000, "gdp": 370900000000, "hdi": 0.699, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 140, "name": "Poland", "lgbt_legal_protections": False, "population": 37887768, "gdp": 632600000000, "hdi": 0.871, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 141, "name": "Portugal", "lgbt_legal_protections": True, "population": 10191409, "gdp": 237900000000, "hdi": 0.864, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 142, "name": "Qatar", "lgbt_legal_protections": False, "population": 2832067, "gdp": 179900000000, "hdi": 0.854, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 143, "name": "Romania", "lgbt_legal_protections": False, "population": 19286123, "gdp": 276200000000, "hdi": 0.825, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 144, "name": "Russia", "lgbt_legal_protections": False, "population": 144373535, "gdp": 1700000000000, "hdi": 0.824, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 145, "name": "Rwanda", "lgbt_legal_protections": False, "population": 13005303, "gdp": 10200000000, "hdi": 0.543, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 146, "name": "Saint Kitts and Nevis", "lgbt_legal_protections": False, "population": 53192, "gdp": 800000000, "hdi": 0.779, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 147, "name": "Saint Lucia", "lgbt_legal_protections": False, "population": 184400, "gdp": 2000000000, "hdi": 0.748, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 148, "name": "Saint Vincent and the Grenadines", "lgbt_legal_protections": False, "population": 110000, "gdp": 800000000, "hdi": 0.723, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 149, "name": "Samoa", "lgbt_legal_protections": False, "population": 199052, "gdp": 800000000, "hdi": 0.717, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 150, "name": "San Marino", "lgbt_legal_protections": True, "population": 34786, "gdp": 2400000000, "hdi": 0.853, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 151, "name": "Sao Tome and Principe", "lgbt_legal_protections": False, "population": 233997, "gdp": 400000000, "hdi": 0.611, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 152, "name": "Saudi Arabia", "lgbt_legal_protections": False, "population": 34813871, "gdp": 794400000000, "hdi": 0.853, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 153, "name": "Senegal", "lgbt_legal_protections": False, "population": 16743930, "gdp": 27400000000, "hdi": 0.505, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 154, "name": "Serbia", "lgbt_legal_protections": False, "population": 6963764, "gdp": 44600000000, "hdi": 0.804, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 155, "name": "Seychelles", "lgbt_legal_protections": False, "population": 98347, "gdp": 1500000000, "hdi": 0.797, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 156, "name": "Sierra Leone", "lgbt_legal_protections": False, "population": 7976985, "gdp": 4100000000, "hdi": 0.438, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 157, "name": "Singapore", "lgbt_legal_protections": False, "population": 5896684, "gdp": 376300000000, "hdi": 0.938, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 158, "name": "Slovakia", "lgbt_legal_protections": False, "population": 5457013, "gdp": 111300000000, "hdi": 0.863, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 159, "name": "Slovenia", "lgbt_legal_protections": True, "population": 2078938, "gdp": 59300000000, "hdi": 0.897, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 160, "name": "Solomon Islands", "lgbt_legal_protections": False, "population": 704116, "gdp": 1500000000, "hdi": 0.546, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 161, "name": "Somalia", "lgbt_legal_protections": False, "population": 16630000, "gdp": 7628000000, "hdi": 0.361, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 162, "name": "South Africa", "lgbt_legal_protections": True, "population": 59799800, "gdp": 385200000000, "hdi": 0.709, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 163, "name": "South Korea", "lgbt_legal_protections": False, "population": 51780579, "gdp": 1600000000000, "hdi": 0.916, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 164, "name": "South Sudan", "lgbt_legal_protections": False, "population": 11892934, "gdp": 1700000000, "hdi": 0.445, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 165, "name": "Spain", "lgbt_legal_protections": True, "population": 46733038, "gdp": 1400000000000, "hdi": 0.906, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 166, "name": "Sri Lanka", "lgbt_legal_protections": False, "population": 21803000, "gdp": 84000000000, "hdi": 0.782, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 167, "name": "Sudan", "lgbt_legal_protections": False, "population": 43849260, "gdp": 34330000000, "hdi": 0.510, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 168, "name": "Suriname", "lgbt_legal_protections": False, "population": 591919, "gdp": 4700000000, "hdi": 0.735, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 169, "name": "Sweden", "lgbt_legal_protections": True, "population": 10175214, "gdp": 538200000000, "hdi": 0.945, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 170, "name": "Switzerland", "lgbt_legal_protections": True, "population": 8715620, "gdp": 707000000000, "hdi": 0.955, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 171, "name": "Syria", "lgbt_legal_protections": False, "population": 17070135, "gdp": 11080000000, "hdi": 0.577, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 172, "name": "Taiwan", "lgbt_legal_protections": True, "population": 23570000, "gdp": 716400000000, "hdi": 0.926, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 173, "name": "Tajikistan", "lgbt_legal_protections": False, "population": 9788774, "gdp": 7000000000, "hdi": 0.669, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 174, "name": "Tanzania", "lgbt_legal_protections": False, "population": 59734218, "gdp": 63200000000, "hdi": 0.536, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 175, "name": "Thailand", "lgbt_legal_protections": True, "population": 69950851, "gdp": 546300000000, "hdi": 0.765, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 176, "name": "Timor-Leste (formerly East Timor)", "lgbt_legal_protections": False, "population": 1324094, "gdp": 2300000000, "hdi": 0.606, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 177, "name": "Togo", "lgbt_legal_protections": False, "population": 8278724, "gdp": 6500000000, "hdi": 0.527, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 178, "name": "Tonga", "lgbt_legal_protections": False, "population": 103197, "gdp": 500000000, "hdi": 0.717, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 179, "name": "Trinidad and Tobago", "lgbt_legal_protections": False, "population": 1394973, "gdp": 22500000000, "hdi": 0.784, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 180, "name": "Tunisia", "lgbt_legal_protections": False, "population": 11818618, "gdp": 42100000000, "hdi": 0.735, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 181, "name": "Turkey", "lgbt_legal_protections": False, "population": 84339067, "gdp": 797200000000, "hdi": 0.820, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 182, "name": "Turkmenistan", "lgbt_legal_protections": False, "population": 6031187, "gdp": 41700000000, "hdi": 0.720, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 183, "name": "Tuvalu", "lgbt_legal_protections": False, "population": 11792, "gdp": 0, "hdi": 0.641, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 184, "name": "Uganda", "lgbt_legal_protections": False, "population": 45741007, "gdp": 34300000000, "hdi": 0.528, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 185, "name": "Ukraine", "lgbt_legal_protections": False, "population": 43733762, "gdp": 161400000000, "hdi": 0.750, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 186, "name": "United Arab Emirates", "lgbt_legal_protections": False, "population": 9890400, "gdp": 421100000000, "hdi": 0.866, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 187, "name": "United Kingdom", "lgbt_legal_protections": True, "population": 68207114, "gdp": 2700000000000, "hdi": 0.932, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 188, "name": "United States of America", "lgbt_legal_protections": False, "population": 332915073, "gdp": 22700000000000, "hdi": 0.926, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 189, "name": "Uruguay", "lgbt_legal_protections": True, "population": 3461734, "gdp": 59200000000, "hdi": 0.804, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 190, "name": "Uzbekistan", "lgbt_legal_protections": False, "population": 33943532, "gdp": 59300000000, "hdi": 0.720, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 191, "name": "Vanuatu", "lgbt_legal_protections": False, "population": 307145, "gdp": 800000000, "hdi": 0.603, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 192, "name": "Vatican City (Holy See)", "lgbt_legal_protections": False, "population": 825, "gdp": 21200000, "hdi": 0.924, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 193, "name": "Venezuela", "lgbt_legal_protections": False, "population": 28435943, "gdp": 23500000000, "hdi": 0.711, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 194, "name": "Vietnam", "lgbt_legal_protections": False, "population": 98168829, "gdp": 343800000000, "hdi": 0.704, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 195, "name": "Yemen", "lgbt_legal_protections": False, "population": 29825968, "gdp": 21610000000, "hdi": 0.470, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 196, "name": "Zambia", "lgbt_legal_protections": False, "population": 18920648, "gdp": 16500000000, "hdi": 0.580, "safety_rating": None, "tourism_rating": None, "overall_rating": None},
        {"id": 197, "name": "Zimbabwe", "lgbt_legal_protections": False, "population": 15092971, "gdp": 24600000000, "hdi": 0.571, "safety_rating": None, "tourism_rating": None, "overall_rating": None}
    ]
    for data in countries_data:
        country = Country(**data)
        db.session.add(country)
    db.session.commit()
    print("Table seeded!")

@app.cli.command("seed_users")
def seed_users():
    user1 = User(
        name = 'Connor',
        email = 'connor.hay.1998@gmail.com',
        password = '123456',
        admin = True
    )
    db.session.add(user1)
    
    user2 = User()
    user2.name = 'Akash'
    user2.email = 'akash@akash.com'
    user2.password = '123456'
    user2.admin = False
    db.session.add(user2)

    user3 = User()
    user3.name = 'Jairo'
    user3.email = 'jairo@jairo.com'
    user3.password = '123456'
    user3.admin = False
    db.session.add(user3)
    db.session.commit()
    print("Table seeded!")


#routes

secret = 'super-secret'
hashing_algo = 'HS256'
payload = None

def make_secure(func):
    @functools.wraps(func)
    def decorator():
        try:
            global payload
            payload = decode_token(request.headers['Authorization'].replace('Bearer ', ''))
            return func()
        except:
            return jsonify(message="You are not authenticated")
    return decorator


def create_token(payload):
    return jwt.encode(payload, secret, algorithm=hashing_algo)

def decode_token(token):
    return jwt.decode(token, secret, algorithms=[hashing_algo])


@app.get("/")
@make_secure
def home():
    return jsonify(message="You are in the home page.", payload=payload)
    

@app.post("/login")
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    token = create_token({username: username, "password": password})
    return jsonify(message="You are now loggied in", token=token)

# Get all countries and assosiated info
@app.route('/countries', methods=['GET'])
def get_all_countries():
    countries = Country.query.all()
    country_schema = CountrySchema(many=True)
    result = country_schema.dump(countries)
    return jsonify(result)

# Get all Users and assosiated info
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users, many=True)
    return jsonify(output)

# Get names for all countries
@app.route('/country_name', methods=['GET'])
def get_country_names():
    countries = Country.query.all()
    country_names = [country.name for country in countries]
    return jsonify(country_names)

# Get GDP for all countries
@app.route('/country_gdp', methods=['GET'])
def get_country_gdp():
    countries = Country.query.all()
    country_gdp = [country.gdp for country in countries]
    return jsonify(country_gdp)

# Get HDI for all countries
@app.route('/country_hdi', methods=['GET'])
def get_country_hdi():
    countries = Country.query.all()
    country_hdi = [country.hdi for country in countries]
    return jsonify(country_hdi)

# Get country and all of it's info
@app.route('/countries/<string:country_name>', methods=['GET'])
def get_country(country_name):
    country = Country.query.filter(Country.name.ilike(country_name)).first()
    if country:
        country_schema = CountrySchema()
        output = country_schema.dump(country)
        return jsonify(output)
    else:
        return jsonify({'message': 'Country not found'})



if __name__ == '__main__':
    app.run(debug=True)



