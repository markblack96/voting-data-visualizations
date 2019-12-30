# We've got some comma separated values, but this is trashy and not good for an API
# So what do we do? A sqlite database, of course!

# We need tables for:
# Congresspersons, political party codes, votes, congresses(?)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from models import Congressperson, Party
import pandas as pd
from models import Base


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

# create first congress
first_congress = members.loc[members['congress'] == 1]
for i in range(len(first_congress)):
    con = Congressperson(icpsr=int(first_congress.loc[i].icpsr), bioname=first_congress.loc[i].bioname)
    session.add(con)

# throw all the parties into the db
unique_parties = parties.drop_duplicates(['party_code'])[['party_code', 'party_name']].reset_index() # have to do that or the following won't run
for i in range(len(unique_parties)):
    p = Party(party_code=int(unique_parties.loc[i].party_code), party_name=unique_parties.loc[i].party_name)
    session.add(p)

# now we want to go through the congress and assign parties
cons = session.query(Congressperson).all()
ps = session.query(Party).all()

for p in ps:
    for con in cons:
        # if con in p:  Need ta figure out how best to do this!
        #   p.append(con)

session.commit()
session.close()
