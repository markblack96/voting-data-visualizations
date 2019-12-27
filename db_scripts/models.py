# Here's where we're going to place our models, for use in our DB conversion script and later in the API
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Congressperson(Base):
    __tablename__ = 'congressperson'
    id = Column(Integer, primary_key=True)
    bioname = Column(String)


class Party(Base):
    __tablename__ = 'party'
    party_code = Column(Integer, primary_key=True)
    name = Column(String)
    members = relationship('congressperson')

class CongresspersonParty(Base): # this could probably be just a Table('association', ...), something to look into
    __tablename__ = 'congressperson_party'
    congressperson_id = Column(Integer, ForeignKey('congressperson.id'), primary_key=True)
    party_code = Column(Integer, ForeignKey('party.party_code'), primary_key=True)
