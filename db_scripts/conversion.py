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
from models import Congressperson, Party
import pandas as pd


engine = create_engine('sqlite://')
members = pd.read_csv('./data/HSall_members.csv')

# Create table for Congressperson
def create_congressperson_table(congresspersons):
    """
    Returns a list of Congressperson objects from a Series as input 
    """
    cons = []
    for i, c in congresspersons:
        cons.append(Congressperson(id=i, bioname=c))
    return cons

# Create table for Party
def create_party_table(parties):
    """
    Returns a list of Party objects from a Dataframe as input
    """
    parties = []


