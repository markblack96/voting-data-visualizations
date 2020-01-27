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

# go through each congress and add a congressperson entity
congresses = members['congress'].unique()
for congress in congresses:
    congresspeople = members[members['congress']==congress]
    # go through each congressperson
    for congressperson in congresspeople:
        con = Congressperson(icpsr=
