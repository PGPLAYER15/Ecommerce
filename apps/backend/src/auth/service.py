from typing import List, Optional
from fastapi import Depends
from auth.models import User
from auth.schemas import UserRegister, UserLogin
from auth.repository import UserAuthRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from shared.security import verify_password
from shared.database import get_db


class UserAuthService:
    def __init__(self, user_repo: UserAuthRepository) -> None:
        self.user_repo = user_repo
        
    async def create_user(self, user_data: UserRegister) -> User:
        """
        Crea un nuevo usuario después de verificar que el email no exista previamente.

        Args:
            user_data (UserRegister): Datos del usuario a registrar.

        Returns:
            User: Usuario creado y persistido en la base de datos.

        Raises:
            ValueError: Si el email ya existe en la base de datos.
        """
        existing_user = await self.user_repo.existing_user(user_data.email)
        
        if existing_user:
            raise ValueError("El email ya existe")
        
        return await self.user_repo.create_user(user_data)

    # Autentica a un usuario verificando su email y contraseña.

    async def authenticate_user(self, email: str, password: str):
        """
        Args:
            email (str): Correo electrónico del usuario.
            password (str): Contraseña proporcionada por el usuario.

        Returns:
            User: Usuario autenticado si las credenciales son correctas, de lo contrario None.
        """
        user = await self.user_repo.get_by_email(email)
        
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        
        return user

def get_user_service(db: Session = Depends(get_db)) -> UserAuthService:
    """
    Proporciona una instancia de UserAuthService con la dependencia de base de datos.

    Args:
        db (Session): Sesión de base de datos proporcionada por la dependencia.

    Returns:
        UserAuthService: Servicio de autenticación de usuario.
    """
    user_repo = UserAuthRepository(db)
    return UserAuthService(user_repo)
