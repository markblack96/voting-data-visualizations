from db_scripts.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def make_sesh():
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    sesh = Session()
    return sesh
