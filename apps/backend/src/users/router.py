"""
Router para la gestión de usuarios del sistema de e-commerce.

Este módulo contiene todos los endpoints relacionados con las operaciones de usuarios,
incluyendo gestión de perfiles, operaciones administrativas y autenticación.
"""

# Importaciones de esquemas y tipos de usuarios
from users.schemas import UserResponse, UserUpdate, UserListResponse
from typing import Optional

# Importaciones de excepciones personalizadas
from users.exceptions import *
from shared.exceptions import UserNotFoundException

# Importaciones de FastAPI y dependencias
from fastapi import APIRouter, HTTPException, status, Depends, Query

# Importaciones de autenticación y modelos
from auth.models import User
from auth.dependencies import get_current_user

# Importaciones de servicios de usuarios
from users.service import UserService, get_user_service

import logging 

# Configuración del logger para este módulo
logger = logging.getLogger(__name__)

# Configuración del router con etiquetas para documentación automática
router = APIRouter(tags=["User"])

# ==================== ENDPOINTS USUARIOS ==================== #

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Obtiene el perfil del usuario autenticado actualmente.
    
    Este endpoint permite a cualquier usuario autenticado obtener su propia información
    de perfil, incluyendo datos personales, configuraciones y estado de la cuenta.
    
    Args:
        current_user (User): Usuario autenticado obtenido del token JWT
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserResponse: Información completa del perfil del usuario
        
    Raises:
        401: Si el token es inválido o ha expirado
        404: Si el usuario no existe en la base de datos
    
    Example:
        GET /users/me
        Authorization: Bearer <token>
        
        Response:
        {
            "id": "uuid",
            "email": "user@example.com",
            "name": "John Doe",
            "role": "user",
            "is_active": true,
            ...
        }
    """
    logger.info(f"Obteniendo el perfil del usuario: {current_user.id}")
    
    # Obtener información completa del usuario desde la base de datos
    user = await user_service.get_by_id(current_user.id)
    return user 

@router.put("/me", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def update_current_user_profile(
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza el perfil del usuario autenticado actualmente.
    
    Permite a un usuario modificar su información personal como nombre, email,
    teléfono, dirección y otros datos del perfil.
    
    Args:
        user_data (UserUpdate): Datos a actualizar del usuario
        user_service (UserService): Servicio de usuarios inyectado por dependencia
        current_user (User): Usuario autenticado obtenido del token JWT
    
    Returns:
        UserResponse: Información actualizada del usuario
        
    Raises:
        400: Si los datos proporcionados son inválidos
        401: Si el token es inválido o ha expirado
        422: Si hay errores de validación en los datos
    
    Example:
        PUT /users/me
        Authorization: Bearer <token>
        
        Body:
        {
            "name": "New Name",
            "email": "newemail@example.com",
            "phone": "1234567890"
        }
    """
    logger.info(f"Actualizando perfil del usuario: {current_user.id}")
    
    # Validar y actualizar los datos del usuario
    update_user = await user_service.update_profile(current_user.id, user_data)
    return update_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Elimina permanentemente la cuenta del usuario autenticado.
    
    Esta operación es irreversible y eliminará todos los datos asociados
    al usuario, incluyendo pedidos, carrito de compras y configuraciones.
    
    Args:
        current_user (User): Usuario autenticado obtenido del token JWT
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        None: Respuesta vacía con código 204
        
    Raises:
        401: Si el token es inválido o ha expirado
        404: Si el usuario no existe en la base de datos
        500: Si ocurre un error durante la eliminación
    
    Example:
        DELETE /users/me
        Authorization: Bearer <token>
        
        Response: 204 No Content
    """
    logger.warning(f"Eliminando cuenta del usuario: {current_user.id}")
    
    # Eliminar el usuario y todos sus datos relacionados
    await user_service.delete_user(current_user.id)
    return

# ==================== ENDPOINTS ADMINISTRATIVOS ==================== # 

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Obtiene la información de un usuario específico por su ID (solo administradores).
    
    Este endpoint permite a los administradores acceder a la información
    completa de cualquier usuario del sistema.
    
    Args:
        user_id (int): ID del usuario a consultar
        current_user (User): Usuario autenticado (debe ser administrador)
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserResponse: Información completa del usuario consultado
        
    Raises:
        401: Si no está autenticado
        403: Si no tiene permisos de administrador
        404: Si el usuario no existe
    
    Example:
        GET /users/123
        Authorization: Bearer <admin_token>
    """
    # Verificar que el usuario actual tiene permisos de administrador
    await user_service.check_admin_permission(current_user.id)
    
    logger.info(f"Admin {current_user.id} accediendo a un usuario por id")
    
    # Obtener el usuario solicitado por ID
    user = await user_service.get_by_id(id=user_id)
    return user

@router.get("/users", response_model=UserListResponse, status_code=status.HTTP_200_OK)
async def list_users(
    skip: int = Query(0, ge=0, description="Numero de registros maximos a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Numero meximo de registros"),
    search: Optional[str] = Query(None, description="Buscar por email o por nombre"),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Lista todos los usuarios del sistema con paginación y búsqueda (solo administradores).
    
    Permite a los administradores obtener una lista paginada de usuarios
    con capacidad de búsqueda por email o nombre.
    
    Args:
        skip (int): Número de registros a saltar para paginación (default: 0)
        limit (int): Número máximo de registros a retornar (default: 10, max: 100)
        search (str, optional): Término de búsqueda para filtrar por email o nombre
        current_user (User): Usuario autenticado (debe ser administrador)
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserListResponse: Lista paginada de usuarios con metadatos
        
    Raises:
        401: Si no está autenticado
        403: Si no tiene permisos de administrador
        422: Si los parámetros de paginación son inválidos
    
    Example:
        GET /users/users?skip=0&limit=10&search=john
        Authorization: Bearer <admin_token>
        
        Response:
        {
            "users": [...],
            "total": 50,
            "skip": 0,
            "limit": 10
        }
    """
    # Verificar permisos de administrador
    await user_service.check_admin_permission(current_user.id)
    
    logger.info(f"Admin {current_user.id} listando usuarios - skip{skip}, limit{limit}")
    
    # Obtener lista paginada de usuarios
    users = await user_service.list_users(skip=skip, limit=limit, search=search)
    return users

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Actualiza la información de un usuario específico por su ID (solo administradores).
    
    Permite a los administradores modificar la información de cualquier usuario
    del sistema, incluyendo datos personales y configuraciones.
    
    Args:
        user_id (int): ID del usuario a actualizar
        user_data (UserUpdate): Datos a actualizar del usuario
        current_user (User): Usuario autenticado (debe ser administrador)
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserResponse: Información actualizada del usuario
        
    Raises:
        401: Si no está autenticado
        403: Si no tiene permisos de administrador
        404: Si el usuario no existe
        422: Si hay errores de validación en los datos
    
    Example:
        PUT /users/123
        Authorization: Bearer <admin_token>
        
        Body:
        {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
    """
    # Verificar permisos de administrador
    await user_service.check_admin_permission(current_user.id)
    
    logger.info(f"Admin {current_user.id} actualizando un usuario")
    
    # Actualizar el perfil del usuario especificado
    user_updated = await user_service.update_profile(user_id=user_id, profile_data=user_data.dict())
    return user_updated

@router.patch("/{user_id}/role", response_model=UserUpdate, status_code=status.HTTP_201_CREATED)
async def change_user_role(
    user_id: int,
    new_role: str,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Cambia el rol de un usuario específico (solo administradores).
    
    Permite a los administradores modificar el rol de cualquier usuario
    del sistema, como cambiar de usuario normal a administrador o viceversa.
    
    Args:
        user_id (int): ID del usuario al que se le cambiará el rol
        new_role (str): Nuevo rol a asignar (ej: "admin", "user", "moderator")
        current_user (User): Usuario autenticado (debe ser administrador)
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserUpdate: Datos actualizados del usuario con el nuevo rol
        
    Raises:
        401: Si no está autenticado
        403: Si no tiene permisos de administrador
        404: Si el usuario no existe
        400: Si el rol especificado no es válido
    
    Example:
        PATCH /users/123/role?new_role=admin
        Authorization: Bearer <admin_token>
    """
    # Verificar permisos de administrador
    await user_service.check_admin_permission(current_user.id)
    
    # Verificar que el rol solicitado existe y es válido
    exist_role = await user_service.verify_role_change(new_role)
    
    logger.info(f"Admin {current_user.id} cambiando rol a un usuario")
    
    # Si el rol no existe, registrar el error y continuar con la validación del servicio
    if exist_role:
        logger.info(f"Cambio de rol no permitido, ese rol no existe")

    # Actualizar el rol del usuario
    update_user = await user_service.change_user_role(user_id=user_id, new_role=new_role)
    return update_user

@router.patch("/{user_id}/activate", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Activa la cuenta de un usuario específico (solo administradores).
    
    Permite a los administradores activar cuentas de usuarios que pueden
    haber sido desactivadas por motivos administrativos o de seguridad.
    
    Args:
        user_id (int): ID del usuario a activar
        current_user (User): Usuario autenticado (debe ser administrador)
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserResponse: Información del usuario con estado actualizado
        
    Raises:
        401: Si no está autenticado
        403: Si no tiene permisos de administrador
        404: Si el usuario no existe
        409: Si el usuario ya está activo
    
    Example:
        PATCH /users/123/activate
        Authorization: Bearer <admin_token>
        
        Response:
        {
            "id": 123,
            "is_active": true,
            ...
        }
    """
    # Verificar permisos de administrador
    await user_service.check_admin_permission(current_user.id)
    
    logger.info(f"Admin {current_user.id} activando cuenta")
    
    # Activar la cuenta del usuario especificado
    activated_user = await user_service.activate_user(user_id=user_id)
    return activated_user

@router.patch("/{user_id}/desactivate", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def desactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Desactiva la cuenta de un usuario específico (solo administradores).
    
    Permite a los administradores desactivar cuentas de usuarios por motivos
    administrativos, de seguridad o disciplinarios. Los usuarios desactivados
    no podrán acceder al sistema hasta ser reactivados.
    
    Args:
        user_id (int): ID del usuario a desactivar
        current_user (User): Usuario autenticado (debe ser administrador)
        user_service (UserService): Servicio de usuarios inyectado por dependencia
    
    Returns:
        UserResponse: Información del usuario con estado actualizado
        
    Raises:
        401: Si no está autenticado
        403: Si no tiene permisos de administrador
        404: Si el usuario no existe
        409: Si el usuario ya está desactivado
        400: Si se intenta desactivar un administrador
    
    Example:
        PATCH /users/123/desactivate
        Authorization: Bearer <admin_token>
        
        Response:
        {
            "id": 123,
            "is_active": false,
            ...
        }
    """
    # Verificar permisos de administrador
    await user_service.check_admin_permission(current_user.id)
    
    logger.info(f"Admin {current_user.id} desactivando cuenta")
    
    # Desactivar la cuenta del usuario especificado
    desactivated_user = await user_service.deactivate_user(user_id=user_id)
    return desactivated_user