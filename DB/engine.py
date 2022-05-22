# models.py
import datetime
from sqlalchemy import create_engine
from config import user, password, database, hostname, port
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship

engine = create_engine('sqlite:///college.db', echo=True)

Base = declarative_base()

db_string = "postgresql://{}:{}@{}:{}/{}".format(
    user, password, hostname, port, database
)

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()


# class Film(base):
#     __tablename__ = 'films'
#
#     title = Column(String, primary_key=True)
#     director = Column(String)
#     year = Column(String)

# # Create
# doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")
# session.add(doctor_strange)
# session.commit()
#
# # Read
# films = session.query(Film)
# for film in films:
#     print(film.title)
#
# # Update
# doctor_strange.title = "Some2016Film"
# session.commit()
#
# # Delete
# session.delete(doctor_strange)
# session.commit()
