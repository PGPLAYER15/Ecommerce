from fastapi import HTTPException, status
from pydantic import EmailStr
from auth.models import User
from auth.InterfaceRepo import UserAuthInterface
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from shared.security import hash_password
import logging
from users.repository import UserRepository

logger = logging.getLogger(__name__)

class UserAuthRepository(UserAuthInterface):
    def __init__(self, db: Session):
        """
        Inicializa el repositorio de autenticación de usuarios.

        Args:
            db (Session): Sesión de base de datos SQLAlchemy.
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def get_by_email(self, email: str):
        return await self.user_repo.get_by_email(email)

    async def get_by_id(self, id: int):
        return await self.user_repo.get_by_id(id)

    async def existing_user(self, email: str) -> bool:
        """
        Verifica si un usuario ya existe en la base de datos por su correo electrónico.

        Args:
            user_data (User): Datos del usuario a verificar.
            db (Session): Sesión de base de datos SQLAlchemy.

        Returns:
            bool: True si el usuario no existe.

        Raises:
            HTTPException: Si el correo ya está registrado.
        """
        user_exists = self.db.query(User).filter(User.email == email).first()
    
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya esta registrado"
            )

        return bool(user_exists)

    async def create_user(self, user_data: User) -> User:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            user_data (User): Datos del usuario a crear.
            db (Session): Sesión de base de datos SQLAlchemy.

        Returns:
            User: Usuario creado y persistido en la base de datos.

        Raises:
            HTTPException: Si ocurre un error de integridad o de base de datos.
        """
        try:
            await self.existing_user(user_data.email)
            
            hashed_password = hash_password(user_data.password)
            
            new_user = User(
                name = user_data.name,
                email= user_data.email,
                password = hashed_password,
                role = user_data.role
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            logger.info(f"Usuario registrado exitosamente: {new_user.email}")

            return new_user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"error inesperado en registro {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )