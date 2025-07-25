from datetime import timedelta
from fastapi import APIRouter, HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from auth.schemas import UserLogin,UserRegister,TokenPayload,Token
from auth.models import User
from auth.service import UserAuthService , get_user_service
from users.schemas import UserResponse
from shared.security import create_access_token

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Auth"])


# Este endpoint es para registrar un usuario y autentifica si se a creado  antes o no para poider crearlo 

@router.post("/auth/register" , response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data:UserRegister, user_service:UserAuthService = Depends(get_user_service)):
    try:
        return await user_service.create_user(user_data)  
    except ValueError as e:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail= str(e)
        )

# Este endpoint es para logear el usuario este verifica si los datos enviados por el usuario son correctos

@router.post("/auth/login",response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: UserLogin, user_service: UserAuthService = Depends(get_user_service)):
    user = await user_service.authenticate_user(form_data.email, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username incorrecto o contraseña"
        )

    token_data = TokenPayload(sub=str(user.id),email=user.email, exp=60 * 24, role=user.role)
    access_token = create_access_token(token_data, timedelta(minutes=token_data.exp))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.role
    }

