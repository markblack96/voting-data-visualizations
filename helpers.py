from db_scripts.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

def make_sesh():
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    sesh = Session()
    return sesh

def members():
    return pd.read_csv('data/HSall_members.csv')

def parties():
    return pd.read_csv('data/HSall_parties.csv')
