# TODO: separate routes for pages from routes for API
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
    # todo: put castcodes in a reference table
    cast_codes = {
        0: 'Not a member of the chamber when this vote was taken',
        1: 'Yea',
        2: 'Paired Yea',
        3: 'Announced Yea',
        4: 'Announced Nay',
        5: 'Paired Nay',
        6: 'Nay',
        7: 'Present (some Congresses)',
        8: 'Present (some Congresses)',
        9: 'Not Voting (Abstention)'
    }
    sesh = make_sesh()
    congressperson = sesh.query(Congressperson).filter_by(icpsr=icpsr).first()
    votes = sesh.query(Vote).filter_by(congress_num=congress_num, icpsr=icpsr).all()
    return_data = []
    for vote in votes:
        rollcall = sesh.query(Rollcall).filter_by(rollnumber=vote.rollnumber, congress_num=vote.congress_num, chamber=vote.chamber).first()
        datum = {
            'congressperson': congressperson.bioname,
            'cast': cast_codes[vote.cast_code],
            # bill information
            'yea_count': rollcall.yea_count,
            'nay_count': rollcall.nay_count,
            'dtl_desc': rollcall.dtl_desc,
            'vote_question': rollcall.vote_question,
            'vote_result': rollcall.vote_result,
            'date': rollcall.date,
        }
        return_data.append(datum)
    sesh.close()
    return jsonify(return_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def tester():
    return render_template('test.html')