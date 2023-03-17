import json 
from flask import Flask 
import psycopg2 
import os



app = Flask(__name__)


@app.route('/')
def welcome():
    return "Welcome to the LGBTQI+ Safety Travel API"



if __name__ == '__main__':
    app.run()