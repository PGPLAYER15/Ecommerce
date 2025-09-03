from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from users.router import router as users_router
from shared.exceptions import AppBaseException

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "E-commerce API"}

app.include_router(auth_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler
async def custom_exception_handler(request: Request, exc: AppBaseException):
    """Handler global para todas las excepciones personalizadas"""
        
    # Mapeo de excepciones a códigos HTTP
    exception_status_map = {
        "UserNotFoundException": 404,
        "InvalidCredentialsException": 401,
        "EmailAlreadyExistsException": 409,
        "DuplicateUsernameException": 409,
        "WeakPasswordException": 400,
        "MaxLoginAttemptsException": 429,
        "UserAccountBlockedException": 403,
        "UserNotVerifiedException": 403,
        "InsufficientPermissionsException": 403,
        "UserSessionExpiredException": 401,
        "UserProfileIncompleteException": 400,
        "InvalidUserRoleException": 400,
        "UserDeletionNotAllowedException": 400,
        "ProductNotFoundException": 404,
        "DuplicateProductNameException": 409,
        "InvalidProductPriceException": 400,
        "ProductOutOfStockException": 404,
        "ProductIncompleteException": 400
    }
    
    status_code = exception_status_map.get(
        exc.__class__.__name__, 
        500
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "detail": getattr(exc, 'detail', None)
        }
    )