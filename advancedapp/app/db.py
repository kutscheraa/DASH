# db.py
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create the SQLAlchemy engine
# Replace 'flask_user', 'flask_password', 'db' with the MySQL user, password, and container name respectively
engine = create_engine('mysql+mysqlconnector://flask_user:flask_password@db/flask_db')

# Create a base class for declarative class definitions
Base = declarative_base()

# Define your data model
class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    region = Column(String(30))
    item_type = Column(String(30))
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)