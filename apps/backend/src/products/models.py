from sqlalchemy import Column , Integer , String , DateTime,Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
from sqlalchemy import ForeignKey

Base = declarative_base()

""" Modelo de usuario que se va a validar """

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=True)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")
