from typing import List, Optional
from fastapi import Depends
from auth.models import User
from auth.schemas import UserRegister, UserLogin
from users.repository import UserRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    def __init__(self, user_repo:UserRepository) -> None:
        self.user_repo = user_repo
        
    
    async def get_by_id(self,id:int)-> Optional[User]:
        try:
            user = await self.user_repo.get_by_id(id)
        except SQLAlchemyError:
            pass