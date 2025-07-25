from fastapi import HTTPException, status
from auth.models import User
from users.interface import UserInterface
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class UserRepository(UserInterface):
    def __init__(self,db:Session):
        self.db = db


    async def get_by_id(self,id:int) -> Optional[User]:
        """
        Obtiene un usuario por su id.

        Args:
            email (str): Correo electrónico del usuario.

        Returns:
            Optional[User]: Usuario si existe, de lo contrario None.
        """
        try:
            user = self.db.query(User).filter(User.id == id).first()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    datail="No se pudo encontrar el usuario con ese id"
                )
                
            logger.info(f"Usuario encontrado exitosamente: {user.id}")            
            return user
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error inesperado buscando el usuario por id {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
            
        
    
    async def get_by_email(self, email: str) -> User | None:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            email (str): Correo electrónico del usuario.

        Returns:
            Optional[User]: Usuario si existe, de lo contrario None.
        """
        try:
            user = self.db.query(User).filter(User.email == email).first()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo encontrar el usuario con el email proporcionado"
                )

            logger.info(f"Usuario encontrado exitosamente: {user.email}")            
            return user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error inesperado buscando el usuario por email {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
            
    async def update_user(self, user_data: User,  update_data:dict) -> User:
        """
        Actualiza la información del usuario.
        
        Args:
            user_data (User): Objeto usuario actual.
            new_email (str): Nuevo correo electrónico.
            new_name (str): Nuevo nombre.
            new_direction (str): Nueva dirección.
        
        Returns:
            User: Usuario actualizado.
        """

        try:
            user = await self.get_by_id(user_data.id)

            allowed_fields = {"email","name","direction"}
            
            for field , value in update_data.items():
                if field in allowed_fields and hasattr(user,field):
                    setattr(user,field,value)

            self.db.commit()
            self.db.refresh(user)

            logger.info(f"Usuario actualizado: {user.id}")
            return user

        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error actualizando usuario: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo actualizar el usuario."
            )