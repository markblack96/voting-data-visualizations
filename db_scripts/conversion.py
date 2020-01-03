# We've got some comma separated values, but this is trashy and not good for an API
# So what do we do? A sqlite database, of course!

# We need tables for:
# Congresspersons, political party codes, votes, congresses(?)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import * 
import pandas as pd


engine = create_engine('sqlite:///test.db', echo=True)
members = pd.read_csv('./data/HSall_members.csv')
parties = pd.read_csv('./data/HSall_parties.csv')
Base.metadata.create_all(engine)

# session stuff
Session = sessionmaker(bind=engine)
session = Session()

# add george washington
# george = members.loc[0]
# c = Congressperson(icpsr=int(george.icpsr), bioname=george.bioname)
# session.add(c)

# create states reference table
states = members[['state_abbrev', 'state_icpsr']].drop_duplicates()
for i in range(len(states)):
    state = State(state_icpsr=int(states.iloc[i].state_icpsr), state_abbrev=states.iloc[i].state_abbrev)
    session.add(state)

# create chamber reference table
chambers = members['chamber'].unique()
for i in range(len(chambers)):
    cham = Chamber(chamber_name=chambers[i])
    session.add(cham)

# throw all the parties into the db
unique_parties = parties.drop_duplicates(['party_code'])[['party_code', 'party_name']].reset_index() # have to do that or the following won't run
for i in range(len(unique_parties)):
    p = Party(party_code=int(unique_parties.loc[i].party_code), party_name=unique_parties.loc[i].party_name)
    session.add(p)

"""
One strategy might be to get each instance of a congressperson in a congress by their ICPSR e.g.
icpsr_list = members.icpsr.unique()
for icpsr in icpsr_list:
    etc.

Then it's straightforward to add requisite data for sql conversion
"""

icpsr_list = members.icpsr.unique()
for i in range(len(icpsr_list)):
    # get basic data
    con = Congressperson(
            icpsr=icpsr_list[i], 
            bioname=members[members['icpsr']==icpsr_list[0]].bioname.unique()[0]
    )
    each_congress_served = members[members['icpsr'] == icpsr_list[i]]
    # go through each_congess_served and add relevant data for parties, congresses, and states for con
    for j in range(len(each_congress_served)):
        con_p = CongresspersonParty(
                    icpsr=each_congress_served.iloc[i].icpsr,
                    party_code=each_congress_served.iloc[i].party_code,
                    congress_num=each_congress_served.iloc[i].congress,
                    chamber=each_congress_served.iloc[i].chamber
                )
    

# create first congress
first_congress = members.loc[members['congress'] == 1]
for i in range(len(first_congress)):
    con = Congressperson(icpsr=int(first_congress.loc[i].icpsr), bioname=first_congress.loc[i].bioname)
    session.add(con)

# now we want to go through the congress and assign parties
cons = session.query(Congressperson).all()
ps = session.query(Party).all() # pronounced "peas" or perhaps "piss" but never "pee ess"


for p in ps:
    for con in cons:
        cons_parties = members[members['icpsr'] == con.icpsr].party_code.unique()
        if p.party_code in cons_parties:
            con_p = CongresspersonParty(
                        icpsr=con.icpsr,
                        party_code=p.party_code,
                        congress_num=
                    )

for p in ps:
    for con in cons:
        # get party codes for each congressperson (can be >1)
        cons_parties = members[members['icpsr'] == con.icpsr].party_code.unique()
        if p.party_code in cons_parties:
            p.congresspersons.append(con)
            session.add(p)

states = session.query(State).all()
for state in states:
    for con in cons:
        cons_states = members[members['icpsr'] == con.icpsr].state_icpsr.unique()
        if state.state_icpsr in cons_states:
            state.congresspersons.append(con)
            session.add(state)


session.commit()
session.close()
