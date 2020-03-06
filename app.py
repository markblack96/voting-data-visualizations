# Routes for API will go here
from flask import Flask, render_template, url_for, jsonify
from db_scripts.models import *
from helpers import *


app = Flask(__name__)

# return json data containing relevant facts for each congress
@app.route('/congress/<num>')
def get_by_congress(num):
    sesh = make_sesh()
    # get the relevant data using db query, jsonify it, send it
    chosen_congress = sesh.query(CongresspersonParty).filter_by(congress_num=num).all()
    congress = []
    for con in chosen_congress:
        datum = {
                    'bioname': con.congressperson.bioname,
                    'icpsr': con.congressperson.icpsr,
                    'party': con.party.party_name,
                    'chamber': con.chamber,
                    'state': con.state,
                    'district': con.district
                }
        congress.append(datum)
    sesh.close()
    return jsonify(congress)

@app.route('/votes/<icpsr>/<congress_num>')
def get_votes(icpsr, congress_num):
    pass

@app.route('/')
def index():
    return render_template('index.html')
