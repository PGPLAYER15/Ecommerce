from sqlalchemy import Column , Integer , String , DateTime,Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

""" Modelo de usuario que se va a validar """

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True),default=uuid.uuid4, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    
    name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    
    direction = Column(String(255), nullable=True)
    
    role = Column(String(20), default="user", nullable=False) 
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False) 
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Preparado para relaciones futuras (comentadas por ahora)
    # orders = relationship("Order", back_populates="user")
    # cart = relationship("Cart", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"