from db import Base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

# Define your data model
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    region = Column(String(30))
    item_type = Column(String(30))
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)