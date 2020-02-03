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

session.commit()
session.close()
end = time.time()
time_passed = end - start
print(f"All done! Total time: {time_passed} seconds")

