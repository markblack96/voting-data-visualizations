# Routes for API will go here
from flask import Flask
from db_scripts.models import *
from helpers import *


app = Flask(__name__)

# return json data containing relevant facts for each congress
@app.route('/congress/<num>')
def get_by_congress(num):
    sesh = make_sesh()
    # get the relevant data using db query, jsonify it, send it
    cons = sesh.query(Congressperson)
    
    sesh.close()
    return json()
