from db import Base
from sqlalchemy import Column, String, Integer
from datetime import datetime
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username