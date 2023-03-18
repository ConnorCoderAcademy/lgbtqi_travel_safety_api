import json 
from flask import Flask, jsonify 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import psycopg2 
import os
import click


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://connorhay_dev:123456@localhost:5432/lgbtqi_travel_safety'

db = SQLAlchemy(app)

# Models 

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

# CLI commands
@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("Database created")

@app.cli.command("drop_db")
def drop_db():
    db.drop_all()
    print("Database dropped.")
      
@app.cli.command("seed_name_and_id")
def seed_db():
    countries = [
        {'id': 1, 'name': 'Afghanistan'},
        {'id': 2, 'name': 'Albania'},
        {'id': 3, 'name': 'Algeria'},
        {'id': 4, 'name': 'Andorra'},
        {'id': 5, 'name': 'Angola'},
        {'id': 6, 'name': 'Antigua and Barbuda'},
        {'id': 7, 'name': 'Argentina'},
        {'id': 8, 'name': 'Armenia'},
        {'id': 9, 'name': 'Australia'},
        {'id': 10, 'name': 'Austria'},
        {'id': 11, 'name': 'Azerbaijan'},
        {'id': 12, 'name': 'Bahamas'},
        {'id': 13, 'name': 'Bahrain'},
        {'id': 14, 'name': 'Bangladesh'},
        {'id': 15, 'name': 'Barbados'},
        {'id': 16, 'name': 'Belarus'},
        {'id': 17, 'name': 'Belgium'},
        {'id': 18, 'name': 'Belize'},
        {'id': 19, 'name': 'Benin'},
        {'id': 20, 'name': 'Bhutan'},
        {'id': 21, 'name': 'Bolivia'},
        {'id': 22, 'name': 'Bosnia and Herzegovina'},
        {'id': 23, 'name': 'Botswana'},
        {'id': 24, 'name': 'Brazil'},
        {'id': 25, 'name': 'Brunei'},
        {'id': 26, 'name': 'Bulgaria'},
        {'id': 27, 'name': 'Burkina Faso'},
        {'id': 28, 'name': 'Burundi'},
        {'id': 29, 'name': 'Cabo Verde'},
        {'id': 30, 'name': 'Cambodia'},
        {'id': 31, 'name': 'Cameroon'},
        {'id': 32, 'name': 'Canada'},
        {'id': 33, 'name': 'Central African Republic'},
        {'id': 34, 'name': 'Chad'},
        {'id': 35, 'name': 'Chile'},
        {'id': 36, 'name': 'China'},
        {'id': 37, 'name': 'Colombia'},
        {'id': 38, 'name': 'Comoros'},
        {'id': 39, 'name': 'Congo, Democratic Republic of the'},
        {'id': 40, 'name': 'Congo, Republic of the'},
        {'id': 41, 'name': 'Costa Rica'},
        {'id': 42, 'name': 'Cote d\'Ivoire'},
        {'id': 43, 'name': 'Croatia'},
        {'id': 44, 'name': 'Cuba'},
        {'id': 45, 'name': 'Cyprus'},
        {'id': 46, 'name': 'Czech Republic'},
        {'id': 47, 'name': 'Denmark'},
        {'id': 48, 'name': 'Djibouti'},
        {'id': 49, 'name': 'Dominica'},
        {'id': 50, 'name': 'Dominican Republic'},
        {'id': 51, 'name': 'Ecuador'},
        {'id': 52, 'name': 'Egypt'},
        {'id': 53, 'name': 'El Salvador'},
        {'id': 54, 'name': 'Equatorial Guinea'},
        {'id': 55, 'name': 'Eritrea'},
        {'id': 56, 'name': 'Estonia'},
        {'id': 57, 'name': 'Eswatini (formerly Swaziland)'},
        {'id': 58, 'name': 'Ethiopia'},
        {'id': 59, 'name': 'Fiji'},
        {'id': 60, 'name': 'Finland'},
        {'id': 61, 'name': 'France'},
        {'id': 62, 'name': 'Gabon'},
        {'id': 63, 'name': 'Gambia'},
        {'id': 64, 'name': 'Georgia'},
        {'id': 65, 'name': 'Germany'},
        {'id': 66, 'name': 'Ghana'},
        {'id': 67, 'name': 'Greece'},
        {'id': 68, 'name': 'Grenada'},
        {'id': 69, 'name': 'Guatemala'},
        {'id': 70, 'name': 'Guinea'},
        {'id': 71, 'name': 'Guinea-Bissau'},
        {'id': 72, 'name': 'Guyana'},
        {'id': 73, 'name': 'Haiti'},
        {'id': 74, 'name': 'Honduras'},
        {'id': 75, 'name': 'Hungary'},
        {'id': 76, 'name': 'Iceland'},
        {'id': 77, 'name': 'India'},
        {'id': 78, 'name': 'Indonesia'},
        {'id': 79, 'name': 'Iran'},
        {'id': 80, 'name': 'Iraq'},
        {'id': 81, 'name': 'Ireland'},
        {'id': 82, 'name': 'Israel'},
        {'id': 83, 'name': 'Italy'},
        {'id': 84, 'name': 'Jamaica'},
        {'id': 85, 'name': 'Japan'},
        {'id': 86, 'name': 'Jordan'},
        {'id': 87, 'name': 'Kazakhstan'},
        {'id': 88, 'name': 'Kenya'},
        {'id': 89, 'name': 'Kiribati'},
        {'id': 90, 'name': 'Kosovo'},
        {'id': 91, 'name': 'Kuwait'},
        {'id': 92, 'name': 'Kyrgyzstan'},
        {'id': 93, 'name': 'Laos'},
        {'id': 94, 'name': 'Latvia'},
        {'id': 95, 'name': 'Lebanon'},
        {'id': 96, 'name': 'Lesotho'},
        {'id': 97, 'name': 'Liberia'},
        {'id': 98, 'name': 'Libya'},
        {'id': 99, 'name': 'Liechtenstein'},
        {'id': 100, 'name': 'Lithuania'},
        {'id': 101, 'name': 'Luxembourg'},
        {'id': 102, 'name': 'Madagascar'},
        {'id': 103, 'name': 'Malawi'},
        {'id': 104, 'name': 'Malaysia'},
        {'id': 105, 'name': 'Maldives'},
        {'id': 106, 'name': 'Mali'},
        {'id': 107, 'name': 'Malta'},
        {'id': 108, 'name': 'Marshall Islands'},
        {'id': 109, 'name': 'Mauritania'},
        {'id': 110, 'name': 'Mauritius'},
        {'id': 111, 'name': 'Mexico'},
        {'id': 112, 'name': 'Micronesia (Federated States of)'},
        {'id': 113, 'name': 'Moldova'},
        {'id': 114, 'name': 'Monaco'},
        {'id': 115, 'name': 'Mongolia'},
        {'id': 116, 'name': 'Montenegro'},
        {'id': 117, 'name': 'Morocco'},
        {'id': 118, 'name': 'Mozambique'},
        {'id': 119, 'name': 'Myanmar (formerly Burma)'},
        {'id': 120, 'name': 'Namibia'},
        {'id': 121, 'name': 'Nauru'},
        {'id': 122, 'name': 'Nepal'},
        {'id': 123, 'name': 'Netherlands'},
        {'id': 124, 'name': 'New Zealand'},
        {'id': 125, 'name': 'Nicaragua'},
        {'id': 126, 'name': 'Niger'},
        {'id': 127, 'name': 'Nigeria'},
        {'id': 128, 'name': 'North Korea'},
        {'id': 129, 'name': 'North Macedonia'},
        {'id': 130, 'name': 'Norway'},
        {'id': 131, 'name': 'Oman'},
        {'id': 132, 'name': 'Pakistan'},
        {'id': 133, 'name': 'Palau'},
        {'id': 134, 'name': 'Palestine'},
        {'id': 135, 'name': 'Panama'},
        {'id': 136, 'name': 'Papua New Guinea'},
        {'id': 137, 'name': 'Paraguay'},
        {'id': 138, 'name': 'Peru'},
        {'id': 139, 'name': 'Philippines'},
        {'id': 140, 'name': 'Poland'},
        {'id': 141, 'name': 'Portugal'},
        {'id': 142, 'name': 'Qatar'},
        {'id': 143, 'name': 'Romania'},
        {'id': 144, 'name': 'Russia'},
        {'id': 145, 'name': 'Rwanda'},
        {'id': 146, 'name': 'Saint Kitts and Nevis'},
        {'id': 147, 'name': 'Saint Lucia'},
        {'id': 148, 'name': 'Saint Vincent and the Grenadines'},
        {'id': 149, 'name': 'Samoa'},
        {'id': 150, 'name': 'San Marino'},
        {'id': 151, 'name': 'Sao Tome and Principe'},
        {'id': 152, 'name': 'Saudi Arabia'},
        {'id': 153, 'name': 'Senegal'},
        {'id': 154, 'name': 'Serbia'},
        {'id': 155, 'name': 'Seychelles'},
        {'id': 156, 'name': 'Sierra Leone'},
        {'id': 157, 'name': 'Singapore'},
        {'id': 158, 'name': 'Slovakia'},
        {'id': 159, 'name': 'Slovenia'},
        {'id': 160, 'name': 'Solomon Islands'},
        {'id': 161, 'name': 'Somalia'},
        {'id': 162, 'name': 'South Africa'},
        {'id': 163, 'name': 'South Korea'},
        {'id': 164, 'name': 'South Sudan'},
        {'id': 165, 'name': 'Spain'},
        {'id': 166, 'name': 'Sri Lanka'},
        {'id': 167, 'name': 'Sudan'},
        {'id': 168, 'name': 'Suriname'},
        {'id': 169, 'name': 'Sweden'},
        {'id': 170, 'name': 'Switzerland'},
        {'id': 171, 'name': 'Syria'},
        {'id': 172, 'name': 'Taiwan'},
        {'id': 173, 'name': 'Tajikistan'},
        {'id': 174, 'name': 'Tanzania'},
        {'id': 175, 'name': 'Thailand'},
        {'id': 176, 'name': 'Timor-Leste (East Timor)'},
        {'id': 177, 'name': 'Togo'},
        {'id': 178, 'name': 'Tonga'},
        {'id': 179, 'name': 'Trinidad and Tobago'},
        {'id': 180, 'name': 'Tunisia'},
        {'id': 181, 'name': 'Turkey'},
        {'id': 182, 'name': 'Turkmenistan'},
        {'id': 183, 'name': 'Tuvalu'},
        {'id': 184, 'name': 'Uganda'},
        {'id': 185, 'name': 'Ukraine'},
        {'id': 186, 'name': 'United Arab Emirates (UAE)'},
        {'id': 187, 'name': 'United Kingdom (UK)'},
        {'id': 188, 'name': 'United States of America (USA)'},
        {'id': 189, 'name': 'Uruguay'},
        {'id': 190, 'name': 'Uzbekistan'},
        {'id': 191, 'name': 'Vanuatu'},
        {'id': 192, 'name': 'Vatican City (Holy See)'},
        {'id': 193, 'name': 'Venezuela'},
        {'id': 194, 'name': 'Vietnam'},
        {'id': 195, 'name': 'Yemen'},
        {'id': 196, 'name': 'Zambia'},
        {'id': 197, 'name': 'Zimbabwe'},
    ]
    for country in countries:
        new_country = Country(id=country['id'], name=country['name'])
        db.session.add(new_country)
        db.session.commit()
        print("table seeded")

@app.cli.command("LGBT_legal_protections")

#routes

if __name__ == '__main__':
    app.run()