from passlib.context import CryptContext
from jose import jwt , JWTError
from datetime import datetime , timedelta
from shared.config import settings
from fastapi import HTTPException,status
from auth.schemas import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

""" Esta es una funcion para hashear las contraseñas """

def hash_password(password: str) -> str:
    """ Devuelve la contraseña hasheada """
    return pwd_context.hash(password)

""" Esta funcion nos ayuda a verificar la contraseña """

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifica si la contraseña es correcta comparandola con la contraseña hasheada """
    return pwd_context.verify(plain_password,hashed_password)

""" Esta funcion es para crear un token """

def create_access_token(payload: TokenPayload, expires_delta: timedelta = None):
    to_encode = payload.dict(exclude_unset=True)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode , settings.secret_key, algorithm= settings.algorithm)
    return encoded_jwt

""" Esta funcion es para verificar que el token coincida con la del usuario """

def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        if "sub" not in payload:
            raise JWTError("Campo 'sub' faltando en el token")
        
        token_data = TokenPayload(**payload)
        
        return token_data
        
    except JWTError as e:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al validar el token{str(e)}:"
        )