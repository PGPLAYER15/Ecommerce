from shared.exceptions import AppBaseException

class InvalidCredentialsException(AppBaseException):
    """Se lanza cuando las credenciales son incorrectas."""
    def __init__(self, email: str = None):
        if email:
            self.message = f"Credenciales incorrectas para el email '{email}'"
        else:
            self.message = "Credenciales incorrectas"
        super().__init__(self.message)

class WeakPasswordException(AppBaseException):
    """Se lanza cuando la contraseña no cumple los requisitos de seguridad."""
    def __init__(self, requirements: list = None):
        self.requirements = requirements
        if requirements:
            self.message = f"La contraseña no cumple los requisitos: {', '.join(requirements)}"
        else:
            self.message = "La contraseña no cumple los requisitos de seguridad"
        super().__init__(self.message)

class PasswordExpiredException(AppBaseException):
    """Se lanza cuando la contraseña ha expirado."""
    def __init__(self, user_id: int, expired_days: int = None):
        self.user_id = user_id
        self.expired_days = expired_days
        if expired_days:
            self.message = f"La contraseña del usuario {user_id} expiró hace {expired_days} días"
        else:
            self.message = f"La contraseña del usuario {user_id} ha expirado"
        super().__init__(self.message)

class MaxLoginAttemptsException(AppBaseException):
    """Se lanza cuando se excede el máximo de intentos de login."""
    def __init__(self, email: str, attempts: int = None, lockout_time: int = None):
        self.email = email
        self.attempts = attempts
        self.lockout_time = lockout_time
        if attempts and lockout_time:
            self.message = f"Máximo de {attempts} intentos de login excedido para '{email}'. Bloqueado por {lockout_time} minutos"
        else:
            self.message = f"Máximo de intentos de login excedido para '{email}'"
        super().__init__(self.message)

class InvalidVerificationTokenException(AppBaseException):
    """Se lanza cuando el token de verificación es inválido o ha expirado."""
    def __init__(self, token_type: str = "verificación"):
        self.token_type = token_type
        self.message = f"Token de {token_type} inválido o expirado"
        super().__init__(self.message)

class UserSessionExpiredException(AppBaseException):
    """Se lanza cuando la sesión del usuario ha expirado."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"La sesión del usuario {user_id} ha expirado"
        super().__init__(self.message)

class UserAccountBlockedException(AppBaseException):
    """Se lanza cuando el usuario está bloqueado."""
    def __init__(self, user_id: int, reason: str = None):
        self.user_id = user_id
        self.reason = reason
        if reason:
            self.message = f"Usuario con ID {user_id} está bloqueado. Razón: {reason}"
        else:
            self.message = f"Usuario con ID {user_id} está bloqueado"
        super().__init__(self.message)

class UserNotVerifiedException(AppBaseException):
    """Se lanza cuando el usuario no ha verificado su cuenta."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"El usuario con ID {user_id} no ha verificado su cuenta"
        super().__init__(self.message)