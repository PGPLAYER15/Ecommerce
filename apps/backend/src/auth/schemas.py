from pydantic import BaseModel , ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional

# Token para codificar o decodificar JWT

class TokenPayload(BaseModel):
    sub: str
    email: EmailStr
    role: str
    exp: Optional[int] = Field(default=30)

# Token para respuestas de Login y Refresh 

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

class TokenWithRefresh(Token):
    refresh_token:str
    expires_in: int

# Schemas para la validacion de los usuarios

class UserLogin(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        hide_input_in_errors=True
    )
    email: EmailStr
    password: str = Field(min_length=5, max_length=255)

class UserRegister(BaseModel):  
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra='forbid',
        hide_input_in_errors=True
    )
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=5, max_length=255)
    role: str = Field(default='user')