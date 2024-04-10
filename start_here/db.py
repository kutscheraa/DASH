from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# Create the SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://doadmin:AVNS_IbKFOzKgR7dClGtqzJX@db-mysql-gui-do-user-14112159-0.c.db.ondigitalocean.com:25060/defaultdb')

# Create a base class for declarative class definitions
Base = declarative_base()

from models.order import Order
from models.user import User

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)