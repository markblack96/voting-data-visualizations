from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import pandas as pd
import time


start = time.time()
engine = create_engine('sqlite:///test.db', echo=True)
votes = pd.read_csv('./data/HSall_votes.csv')
rollcalls = pd.read_csv('./data/HSall_rollcalls.csv')
Base.metadata.create_all(engine)

# session stuff
Session = sessionmaker(bind=engine)
session = Session()

