# TODO: don't use ORM for bulk insertions (too slow), use raw sqlite statements (10x faster)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import pandas as pd
import time


start = time.time()
engine = create_engine('sqlite:///test.db', echo=True)
members = pd.read_csv('./data/HSall_members.csv')
parties = pd.read_csv('./data/HSall_parties.csv')
Base.metadata.create_all(engine)

# session stuff
Session = sessionmaker(bind=engine)
session = Session()

# populate states
states = members[['state_abbrev', 'state_icpsr']].drop_duplicates()
for i in range(len(states)):
    state = State(state_icpsr=int(states.iloc[i].state_icpsr), state_abbrev=states.iloc[i].state_abbrev)
    session.add(state)

# populate chambers
chambers = members['chamber'].unique()
for i in range(len(chambers)):
     cham = Chamber(chamber_name=chambers[i])
     session.add(cham)

unique_parties = parties.drop_duplicates(['party_code'])[['party_code', 'party_name']]
for i in range(len(unique_parties)):
     p = Party(party_code=int(unique_parties.iloc[i].party_code), party_name=unique_parties.iloc[i].party_name)
     session.add(p)

# go through each congress and add a congressperson entity
congresses = members['congress'].unique()
for congress in congresses:
    congresspeople = members[members['congress']==congress]
    # go through each congressperson
    for i in range(len(congresspeople)):
        con = congresspeople.iloc[i]
        if len(session.query(Congressperson).filter_by(icpsr=int(con.icpsr)).all()) == 0:
            congressperson = Congressperson(
                                icpsr=int(con.icpsr),
                                bioname=con.bioname
            )
            session.add(congressperson)
        congressperson = session.query(Congressperson).filter_by(icpsr=int(con.icpsr)).first()
        c_p = CongresspersonParty(
                                icpsr=congressperson.icpsr,
                                party_code=int(congresspeople.iloc[i].party_code),
                                congress_num=int(congresspeople.iloc[i].congress),
                                chamber=congresspeople.iloc[i].chamber,
                                state=congresspeople.iloc[i].state_abbrev,
                                district=int(congresspeople.iloc[i].district_code)
        )
        c_p.party = session.query(Party).filter_by(party_code=c_p.party_code).first()
        c_p.congressperson = congressperson
        session.add(c_p)

# add congresspeople to states
cons = session.query(Congressperson).all()
states = session.query(State).all() # this works but is excruciatingly slow b/c cons is huge
for state in states:
    for con in cons:
        cons_states = members[members['icpsr'] == con.icpsr].state_icpsr.unique()
        if state.state_icpsr in cons_states:
            state.congresspersons.append(con)
            session.add(state)
"""
# add votes (this might take a while)
print("About to open HSall_votes")
votes = pd.read_csv('data/HSall_votes.csv') # a hefty boy... >1,000,000 rows, 604 MB of data
print("HSall_votes open, about to open rollcalls")
rollcalls = pd.read_csv('data/HSall_rollcalls.csv', low_memory=False)
print("Rollcalls open")

for i in range(len(votes)):
    v = Vote(congress_num=int(votes.loc[i].congress), 
                chamber=votes.loc[i].chamber, 
                rollnumber=int(votes.loc[i].rollnumber), 
                icpsr=int(votes.loc[i].icpsr), 
                cast_code=int(votes.loc[i].cast_code)
            )
    session.add(v)
    print("Added ", v)
    print(i, "/", len(votes))
    if i%5000 == 0:
        session.commit() # commit so that we don't end up with 24,000,000 rows to commit at once, it will crash otherwise.

for i in range(len(rollcalls)):
    r = Rollcall(
            congress_num = int(rollcalls.loc[i].congress),
            chamber = rollcalls.loc[i].chamber,
            rollnumber = int(rollcalls.loc[i].rollnumber),
            date = rollcalls.loc[i].date,
            session = rollcalls.loc[i].session,
            bill_number = rollcalls.loc[i].bill_number,
            yea_count = int(rollcalls.loc[i].yea_count),
            nay_count = int(rollcalls.loc[i].nay_count),
            vote_result = rollcalls.loc[i].vote_result,
            vote_question = rollcalls.loc[i].vote_question,
            dtl_desc = rollcalls.loc[i].dtl_desc
        )
    session.add(r)
    print("Added ", r)
    print(i, "/", len(rollcalls))

"""
session.commit()
session.close()
end = time.time()
time_passed = end - start
print(f"All done! Total time: {time_passed} seconds")
