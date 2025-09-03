from fastapi import HTTPException, status
from users.interface import UserInterface
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from auth.models import User
from shared.exceptions import DatabaseException
from typing import Optional, List
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

            Raises:
                DatabaseException: Si ocurre un error al buscar el usuario.
        """
        try:
            user = self.db.query(User).filter(User.id == id).first()
            
            if user:
                logger.debug(f"Usuario encontrado exitosamente: {user.id}")
            else:
                logger.debug(f"Usuario con ID {id} no encontrado")          
            return user
            
        except SQLAlchemyError as e:
            logger.error(f"Error de BD buscando usuario por ID {id}: {str(e)}")
            raise DatabaseException(f"Error al buscar usuario con ID {id}")
            
        
    
    async def get_by_email(self, email: str) -> User | None:
        """
            Obtiene un usuario por su correo electrónico.

            Args:
                email (str): Correo electrónico del usuario.

            Returns:
                Optional[User]: Usuario si existe, de lo contrario None.

            Raises:
                DatabaseException: Si ocurre un error al buscar el usuario.
        """
        try:
            user = self.db.query(User).filter(User.email == email).first()
            
            if user:
                logger.debug(f"Usuario encontrado por email: {user.email}")
            else:
                logger.debug(f"Usuario con email {email} no encontrado")
                
            return user
            
        except SQLAlchemyError as e:
            logger.error(f"Error de BD buscando usuario por email {email}: {str(e)}")
            raise DatabaseException(f"Error al buscar usuario con email {email}")
            
    async def update_user(self, user: User,  update_data:dict) -> User:
        """
        Actualiza la información del usuario.
        
            Args:
                user_data (User): Objeto usuario actual.
                update_data (Dict): Un diccionario con informacion que se actualizo
            
            Returns:
                User: Usuario actualizado.

            Raises:
                DatabaseException: Si ocurre un error al actualizar el usuario.
        """

        try:
            allowed_fields = {"email", "name", "direction", "phone"}
            
            for field, value in update_data.items():
                if field in allowed_fields and hasattr(user, field) and value is not None:
                    setattr(user, field, value)
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"Usuario actualizado exitosamente: {user.id}")
            return user
            
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad actualizando usuario {user.id}: {str(e)}")
            
            error_msg = str(e).lower()
            if "email" in error_msg:
                raise DatabaseException("El email ya está en uso por otro usuario")
            elif "username" in error_msg:
                raise DatabaseException("El nombre de usuario ya está en uso")
            else:
                raise DatabaseException("Error de integridad en los datos del usuario")
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de BD actualizando usuario {user.id}: {str(e)}")
            raise DatabaseException(f"Error al actualizar usuario {user.id}")
            
    async def delete_user(self,user:User)-> bool:
        """
        Elimina un usuario.

            Args:
                user (User): El usuario a eliminar.

            Returns:
                bool: True si se eliminó exitosamente, False en caso contrario.

            Raises:
                DatabaseException: Si ocurre un error al eliminar el usuario.
        """
        try:
            self.db.delete(user)
            self.db.commit()
            logger.info(f"Usuario eliminado exitosamente: {user.id}")
            return True
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error eliminando usuario {user.id}: {str(e)}")
            raise DatabaseException(f"Error al eliminar usuario {user.id}")
        
    def list_users(self, skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[User]:
        """
            Lista usuarios con paginación y búsqueda opcional.
                    
            Args:
                skip (int): Registros a saltar.
                limit (int): Máximo de registros.
                search (str, optional): Término de búsqueda.
                
            Returns:
                List[User]: Lista de usuarios.

            Raises:
                DatabaseException: Si ocurre un error al listar los usuarios.
        """
        try:
            query = self.db.query(User)
            
            if search:
                search_filter = f"%{search}%"
                query = query.filter(
                    (User.email.ilike(search_filter)) |
                    (User.name.ilike(search_filter)) |
                    (User.first_name.ilike(search_filter)) |
                    (User.last_name.ilike(search_filter))
                )
            
            # Aplicar paginación
            users = query.offset(skip).limit(limit).all()
            
            logger.debug(f"Listando usuarios: skip={skip}, limit={limit}, found={len(users)}")
            return users
            
        except SQLAlchemyError as e:
            logger.error(f"Error listando usuarios: {str(e)}")
            raise DatabaseException("Error al obtener la lista de usuarios")