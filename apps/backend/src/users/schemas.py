from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    # Campos básicoss
    id: UUID
    email: EmailStr
    name: str
    
    # Información personal
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None 
    
    # Sistema
    role: str
    is_active: bool
    is_verified: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid'
    )
    
    # Información básica
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    
    # Información personal
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    phone: Optional[str] = Field(default=None, min_length=10, max_length=20)
    direction: Optional[str] = Field(default=None, min_length=5, max_length=255)
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validación básica de teléfono"""
        if v is not None:
            # Remover espacios y caracteres especiales para validación
            clean_phone = ''.join(filter(str.isdigit, v))
            if len(clean_phone) < 10:
                raise ValueError('Teléfono debe tener al menos 10 dígitos')
        return v

class UserCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid'
    )
    
    # Campos requeridos
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    
    # Campos opcionales
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    direction: Optional[str] = Field(default=None, max_length=255)
    role: Literal["user", "admin"] = Field(default="user")
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

class UserPublic(BaseModel):
    """
    Schema público de usuario (para mostrar en comentarios, etc.).
    Solo información no sensible.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    # No incluir email, teléfono, dirección, etc.

class UserListResponse(BaseModel):
    """
    Schema para listado de usuarios (admin).
    Versión simplificada para listas.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

class UserRoleUpdate(BaseModel):
    """Schema específico para cambio de roles (admin only)"""
    role: Literal["client", "admin"] = Field(...)
    
class UserStatusUpdate(BaseModel):
    """Schema para cambio de estado (admin only)"""
    is_active: bool = Field(...)