# Here's where we're going to place our models, for use in our DB conversion script and later in the API
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

congressperson_party = Table('congressperson_party', Base.metadata,
    Column('icpsr', Integer, ForeignKey('congressperson.icpsr')),
    Column('party_code', Integer, ForeignKey('party.party_code')),
    Column('congress_num', Integer, ForeignKey('congress.congress_num')),
    Column('chamber', String)
)


class Congressperson(Base):
    __tablename__ = 'congressperson'
    icpsr = Column(Integer, primary_key=True) # Note: this is their ICPSR code or whatever
    bioname = Column(String)
    parties = relationship('Party', secondary=congressperson_party, back_populates='congresspersons')
    def __repr__(self):
        return "<Congressperson(bioname='%s')>" % (self.bioname)


class Party(Base):
    __tablename__ = 'party'
    party_code = Column(Integer, primary_key=True)
    party_name = Column(String)
    congresspersons = relationship('Congressperson', secondary=congressperson_party, back_populates='parties')
    def __repr__(self):
        return "<Party(party_name='%s')>" % (self.party_name)


class Congress(Base):
    __tablename__ = 'congress'
    congress_num = Column(Integer, primary_key=True)


class Chamber(Base):
    __tablename__ = 'chamber'
    chamber_name = Column(String, primary_key=True)

class State(Base):
    # yet another reference table!
    __tablename__ = 'states'
    state_icpsr = Column(Integer, primary_key=True)
    state_abbrev = Column(String)
