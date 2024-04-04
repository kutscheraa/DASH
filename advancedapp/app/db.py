# db.py
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

# Create the SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://flask_user:flask_password@db/flask_db')

# Create a base class for declarative class definitions
Base = declarative_base()

from models.order import Order

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)