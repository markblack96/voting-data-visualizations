# Here's where we're going to place our models, for use in our DB conversion script and later in the API
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# todo: make the below into association objects
"""congressperson_party = Table('congressperson_party', Base.metadata,
    Column('icpsr', Integer, ForeignKey('congressperson.icpsr')),
    Column('party_code', Integer, ForeignKey('party.party_code')),
    Column('congress_num', Integer, ForeignKey('congress.congress_num')),
    Column('chamber', String)
)"""

congressperson_state = Table('congressperson_state', Base.metadata,
    Column('state_icpsr', Integer, ForeignKey('state.state_icpsr')),
    Column('congressperson_icpsr', Integer, ForeignKey('congressperson.icpsr'))
)

class CongresspersonParty(Base):
    __tablename__ = 'congressperson_party'
    icpsr = Column(Integer, ForeignKey('congressperson.icpsr'), primary_key=True)
    party_code = Column(Integer, ForeignKey('party.party_code'), primary_key=True)
    party = relationship('Party', back_populates='congresspersons')
    congressperson = relationship('Congressperson', back_populates='parties')
    congress_num = Column(Integer) # todo: probably make this a primary key too, since icpsr+party_code will be insufficient when >1st congress added
    chamber = Column(String)


class Congressperson(Base):
    __tablename__ = 'congressperson'
    icpsr = Column(Integer, primary_key=True) 
    bioname = Column(String)
    parties = relationship('CongresspersonParty', back_populates='congressperson')
    states = relationship('State', secondary=congressperson_state, back_populates='congresspersons')
    def __repr__(self):
        return "<Congressperson(bioname='%s')>" % (self.bioname)


class Party(Base):
    __tablename__ = 'party'
    party_code = Column(Integer, primary_key=True)
    party_name = Column(String)
    congresspersons = relationship('CongresspersonParty', back_populates='party')
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
    __tablename__ = 'state'
    state_icpsr = Column(Integer, primary_key=True)
    state_abbrev = Column(String)
    congresspersons = relationship('Congressperson', secondary=congressperson_state, back_populates='states')

