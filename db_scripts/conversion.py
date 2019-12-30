# We've got some comma separated values, but this is trashy and not good for an API
# So what do we do? A sqlite database, of course!

# We need tables for:
# Congresspersons, political party codes, votes, congresses(?)
# ________________
#| congressperson |
#|----------------|
#|bioname         |
#|party code      |
#------------------
# _______________
#|     vote      |
#|---------------|
#|               |
#-----------------
# And so on

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
george = members.loc[0]
c = Congressperson(icpsr=int(george.icpsr), bioname=george.bioname)
session.add(c)
session.commit()
session.close()
