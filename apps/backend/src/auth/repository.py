from fastapi import HTTPException, status
from apps.backend.src.auth.models import User
from auth.InterfaceRepo import UserRepositoryInterface
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from shared.security import hash_password
import logging

logger = logging.getLogger(__name__)

class UserAuthRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.db.query(User).filter(User.email == email).first()
    
    async def existing_user(self,user_data: User, db: Session) -> bool:
        user_existis = await db.query(User).filter (User.email == user_data.email).first()
    
        if user_existis:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya esta registrado"
            )

        return True

    async def create(self, user_data: User , db: Session) -> User:
        try:
            await self.existing_user(user_data)
            
            
            hashed_password = hash_password(user_data.password)
            
            new_user = User(
                name = user_data.name,
                email= user_data.email,
                password = hashed_password,
                role = user_data.role
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"Usuario registrado exitosamente: {new_user.email}")

        except IntegrityError as e:
            db.rollback()
            logger.error(f"error inesperado en registro {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

