from typing import List, Optional
from fastapi import Depends
from auth.models import User
from shared.database import get_db
from auth.schemas import UserRegister, UserLogin
from users.repository import UserRepository
from users.exceptions import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from shared.exceptions import UserNotFoundException, DatabaseException, InsufficientPermissionsException
import logging

class UserService:
    def __init__(self, user_repo:UserRepository) -> None:
        self.user_repo = user_repo
        self.logger = logging.getLogger(__name__)
        
    def update_profile(self,user_id:int , profile_data:dict):
        user = self.get_by_id(user_id)
        
        if not profile_data:
            raise ValueError("No se proporcionaron datos para actualizar")

        required_for_complete_profile = {"email","name","direction"}
        
        if any(field in profile_data for field in required_for_complete_profile):
            combined_data = {
                "name": profile_data.get("name", user.name),
                "email": profile_data.get("email", user.email), 
                "direction": profile_data.get("direction", user.direction)
            }
            
        missing_fields = [
            field for field in required_for_complete_profile
            if not profile_data.get(field)
        ]
        
        if missing_fields:
            raise UserProfileIncompleteException(
                user_id=user_id,
                missing_fields=missing_fields
        )
    
        try:
            return self.user_repo.update_user(user,profile_data)
        except DatabaseException:
            raise
    
    def get_by_id(self, id: int) -> User:

        if not isinstance(id, int) or id <= 0:
            raise ValueError("El ID debe ser un entero positivo")
        
        try:
            user = self.user_repo.get_by_id(id)
            
            if user is None:
                raise UserNotFoundException(user_id=id)
            
            return user
            
        except UserNotFoundException:
            raise
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error BD al obtener usuario {id}: {str(e)}")
            raise DatabaseException(f"Error al obtener usuario con ID {id}")

    
    def delete_user(self,user_id:int):
        user = self.get_by_id(user_id)
        
        if not user:
            raise UserNotFoundException(user_id)
        
        if user.role == "admin":
            raise UserDeletionNotAllowedException(
                user_id=user_id,
                reason="No se puede eliminar un administrador"
            )
        
        return self.user_repo.delete_user(user)
    
    def list_users(self, skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[User]:
        """
        Lista usuarios con paginación.
        """
        if skip < 0:
            raise ValueError("skip debe ser mayor o igual a 0")
        if limit <= 0 or limit > 100:
            raise ValueError("limit debe estar entre 1 y 100")
        
        return self.user_repo.list_users(skip, limit, search)
    
    def check_admin_permission(self,user_id:int) -> None:
        """
            Verifica si un usuiario tiene permisos de administrador
            
        Args:
            user_id (int): ID del usuario a verificar.
            
        Raises:
            InsufficientPermissionsException: Si no es admin.
        """
        user = self.get_by_id(user_id)
        
        if user.role != "admin":
            raise InsufficientPermissionsException(
                user_id=user_id,
                required_permission="administrador"
            )
            
    def change_user_role(self, user_id: int, new_role: str) -> User:
        """
        Cambia el rol de un usuario.
        
        NUEVO MÉTODO para cambio de roles.
        """
        valid_roles = ["user", "admin", "moderator"]
        
        if new_role not in valid_roles:
            raise InvalidUserRoleException(new_role, valid_roles)
        
        user = self.get_by_id(user_id)
        
        update_data = {"role": new_role}
        return self.user_repo.update_user(user, update_data)
    
    def activate_user(self, user_id: int) -> User:
        """
        Activa un usuario.
        
        """
        user = self.get_by_id(user_id)
        
        if user.is_active:
            raise UserAlreadyActiveException(user_id)
        
        update_data = {"is_active": True}
        return self.user_repo.update_user(user, update_data)

    def deactivate_user(self, user_id: int) -> User:
        """
        Desactiva un usuario.
        """
        user = self.get_by_id(user_id)
        
        if not user.is_active:
            raise UserAlreadyInactiveException(user_id)
        
        update_data = {"is_active": False}
        return self.user_repo.update_user(user, update_data)
    
    def verify_role_change(user_role:str):
        permit_role = ["admin","role"]
        
        if user_role in permit_role:
            return False
        
        return True

def get_user_service(db:Session = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)