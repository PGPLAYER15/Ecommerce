# Token para codificar o decodificar JWT
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, Literal

class TokenPayload(BaseModel):
    """Payload del JWT token"""
    sub: str  # User ID como string
    email: EmailStr
    role: str
    exp: Optional[int] = None

class Token(BaseModel):
    """Respuesta básica de autenticación"""
    access_token: str
    token_type: str = Field(default="bearer")
    user_role: str

class TokenWithRefresh(Token):
    """Token con refresh token incluido"""
    refresh_token: str
    expires_in: int


class UserLogin(BaseModel):
    """Schema para login de usuario"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        hide_input_in_errors=True
    )
    
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)

class UserRegister(BaseModel):
    """Schema para registro de usuario"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        hide_input_in_errors=True
    )
    
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    role: Literal["client", "admin"] = Field(default="client")
    
    @validator('role')
    def validate_role(cls, v):
        """Validación adicional de roles"""
        valid_roles = ["client", "admin"]
        if v not in valid_roles:
            raise ValueError(f'Rol debe ser uno de: {", ".join(valid_roles)}')
        return v