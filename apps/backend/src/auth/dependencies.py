from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from auth.models import User
from shared.security import verify_token
from shared.database import get_db
from auth.schemas import TokenPayload
from auth.exceptions import UserSessionExpiredException, UserNotVerifiedException
from shared.exceptions import UserNotFoundException, InsufficientPermissionsException
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> User:
    
    """
        args: 
        
            db: Sesion de base de datos
            token: Token JWT del usuario

        Returns:
            User: Usuario authenticado
            
        Raises:
            HTTPException: Si el token es invalido o si ya caduco
    """
    
    try:
        payload = verify_token(token)
        
        if not payload.sub or not payload.sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token malformado",
                headers={"WWW-Authenticate":"Bearer"}
            )
            
        try:
            user_id = int(payload.id)
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token malformado",
                headers={"WWW-Authenticate":"Bearer"}
            )
            
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
            
        return user
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario No encontrado"
        )
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate":"Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def get_admin_required(current_user:User = Depends(get_current_user)) -> User:
    """
    Verifica que el usuario actual tenga rol de administrador.
    
    Args:
        current_user: Usuario autenticado obtenido de get_current_user
        
    Returns:
        User: Usuario administrador autenticado
        
    Raises:
        HTTPException: Si el usuario no tiene permisos de administrador o error interno
    """
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso solo para administradores"
            )
            
        return current_user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            datail = "Error interno del servidor"
        )