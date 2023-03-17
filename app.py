import json 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import psycopg2 
import os

#config
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://connorhay:1372@localhost:5432/lgbtqi_travel"
db = SQLAlchemy(app)


class country (db.Model):
    __tablename__ = "countries"
    country_id = db.Column(db.serial, primary_key = True)
    name = db.Column(db.varchar)
    LGBT_legal_protections = db.Column(db.boolean)
    population = db.Column(db.integer)
    GDP = db.Column(db.BigInteger)
    HDI = db.Column(db.decimal(10, 3))
    safety_rating = db.Column(db.Float)
    tourism_rating = db.Column(db.Float)
    overall_rating = db.Column(db.Float)

# CLI commands
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


#routes
@app.route('/')
def welcome():
    return "Welcome to the LGBTQI+ Safety Travel API"



if __name__ == '__main__':
    app.run()