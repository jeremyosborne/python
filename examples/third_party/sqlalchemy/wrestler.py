"""Requires
    
    pip install sqlalchemy
"""

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Turn echo to True to see the created SQL statements.
engine = create_engine('sqlite:///test.db3', echo=False)

# Create a database session (connection) for getting/saving wrestlers.
session = sessionmaker(bind=engine)()

# Allow use of declarative models.
Base = declarative_base(bind=engine)

# Model/db table as Python class.
class Wrestler(Base):
    __tablename__ = 'wrestlers'

    id = Column(Integer, primary_key=True)
    name = Column(String, default="NOBODY", unique=True, nullable=False)
    brawn = Column(Integer, default=5, nullable=False)
    finesse = Column(Integer, default=5, nullable=False)
    wins = Column(Integer, default=0, nullable=False)
    losses = Column(Integer, default=0, nullable=False)
    
    def __repr__(self):
        """Pretty print.
        """
        return "(%s) %s" % (self.id, self.name)

# Create the tables if they don't exist.
Base.metadata.create_all()



# Create a default wrestler. This will error out if done more than once.
print "Creating a default wrestler."
try:
    # Create in memory.
    w = Wrestler()
    # Queue up for saving.
    session.add(w)
    # Save/update.
    session.commit()
    print "Created a default wrestler."
except sqlalchemy.exc.SQLAlchemyError as err:
    print "Can't add the default wrestler, probably already added."
    # cleanup addition that cannot be made.
    session.rollback()



print "Adding a wrestler with the name Nacho."
try:
    w = Wrestler(name="Nacho")
    session.add(w)
    session.commit()
    print "Nacho added to db."
except sqlalchemy.exc.SQLAlchemyError as err:
    print "Can't add Nacho, probably already exists in db."
    # cleanup addition that cannot be made.
    session.rollback()


print "Getting a list of all the wrestlers."
print session.query(Wrestler).all()

print "Getting a count of all of the wrestlers."
print session.query(Wrestler).count()

print "Getting the wrestler(s) with names like Nacho."
print session.query(Wrestler).filter(Wrestler.name.like("%Nacho%")).all()

print "Getting the first (and should be only) wrestler named Nacho"
print session.query(Wrestler).filter(Wrestler.name == "Nacho").first()

print "Get the Nacho wrestler and do some things to him."
nacho = session.query(Wrestler).filter(Wrestler.name == "Nacho").first()

print "Increase his wins."
nacho.wins += 1

print "Format him into a string."
print "{0.name} has {0.wins} wins and {0.losses} losses.".format(nacho)

print "Update the database with the changes."
#session.add(nacho)
session.commit()

print "Increase Nacho's losses."
nacho.losses += 1

print "How many losses does the in memory model have?"
print nacho.losses

print "What models are set to be cmmitted?"
print session.dirty

print "Nevermind, Nacho never loses. Rollback changes (just to Nacho)."
session.refresh(nacho)

print "How many losses does Nacho now have?"
print nacho.losses

print "Are there any pending database updates?"
print session.dirty

