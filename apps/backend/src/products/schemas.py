from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    # Campos Basicos
    id: UUID
    name: str
    description: Optional[str] = None
    price: int
    image_url: Optional[str] = None
    stock: int
    
    #Sistemma
    is_active: bool
    created_at: datetime
    
    # Relación con categoría
    category_id: UUID
    category_name: str
    

class ProductUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[int] = Field(default=None, gt=0)
    image_url: Optional[str] = Field(default=None, max_length=255)
    stock: Optional[int] = Field(default=None, ge=0)

    def validate_price(cls, v):
        """Validación del precio"""
        if v is not None and v <= 0:
            raise ValueError("El precio deberia ser mas alto que 0 o 10")
        return v

class ProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)
    price: int = Field(..., gt=0)
    image_url: Optional[str] = Field(default=None, max_length=255)
    stock: int = Field(..., ge=0)

    def validate_price(cls, v):
        """Validación del precio"""
        if v is not None and v <= 0:
            raise ValueError("El precio deberia ser mas alto que 0 o 10")
        return v

class ProductListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    price: int
    image_url: Optional[str] = None
    stock: int
    is_active: bool