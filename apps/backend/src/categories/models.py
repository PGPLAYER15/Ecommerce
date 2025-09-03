from sqlalchemy import Column , Integer , String , DateTime,Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
from sqlalchemy import ForeignKey

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    products = relationship("Product", back_populates="category")
