from typing import List, Optional
from auth.models import User
from auth.schemas import UserRegister, UserLogin
from auth.repository import UserAuthRepository
from sqlalchemy.exc import SQLAlchemyError
from shared.security import verify_password

class UserAuthService:
    def __init__(self,user_repo:UserAuthRepository) -> None:
        self.user_repo = user_repo
        
    """ Funcion de servicios para crear usuarios """
        
    async def create_user(self, user_data: UserRegister) -> User:
        existing_user = await self.user_repo.existing_user(user_data.email)
        
        if existing_user:
            raise ValueError("El email ya existe")
        
        return await self.user_repo.create(user_data)

    async def authenticate_user(self, email: str,password:str):
        user = await self.user_repo.get_by_email(email)
        
        if not user:
            return None
        if not verify_password(password , user.password):
            return None
        
        return user