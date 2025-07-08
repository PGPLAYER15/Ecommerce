from sqlalchemy import Column , Integer , String , DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

""" Modelo de usuario que se va a validar """

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index = True)
    name = Column(String(50),nullable=False)
    email = Column(String(255),unique=True,nullable=False,index=True)
    password = Column(String(255),nullable=False)
    role = Column(String(20),default="user")
    created_at = Column(DateTime, default=datetime.utcnow)