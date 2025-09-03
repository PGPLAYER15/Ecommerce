from shared.exceptions import AppBaseException

class EmailAlreadyExistsException(AppBaseException):
    """Se lanza cuando el email ya está registrado."""
    def __init__(self, email: str):
        self.email = email
        self.message = f"El email '{email}' ya está en uso"
        super().__init__(self.message)

class DuplicateUsernameException(AppBaseException):
    """Se lanza cuando el nombre de usuario ya existe."""
    def __init__(self, username: str):
        self.username = username
        self.message = f"El nombre de usuario '{username}' ya está en uso"
        super().__init__(self.message)

class UserAlreadyActiveException(AppBaseException):
    """Se lanza cuando se intenta activar un usuario ya activo."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"El usuario con ID {user_id} ya está activo"
        super().__init__(self.message)

class UserAlreadyInactiveException(AppBaseException):
    """Se lanza cuando se intenta desactivar un usuario ya inactivo."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"El usuario con ID {user_id} ya está inactivo"
        super().__init__(self.message)

class InvalidUserRoleException(AppBaseException):
    """Se lanza cuando se asigna un rol inválido."""
    def __init__(self, role: str, valid_roles: list = None):
        self.role = role
        self.valid_roles = valid_roles
        if valid_roles:
            self.message = f"Rol '{role}' inválido. Roles válidos: {', '.join(valid_roles)}"
        else:
            self.message = f"Rol '{role}' inválido"
        super().__init__(self.message)

class UserProfileIncompleteException(AppBaseException):
    """Se lanza cuando el perfil del usuario está incompleto."""
    def __init__(self, user_id: int, missing_fields: list = None):
        self.user_id = user_id
        self.missing_fields = missing_fields
        if missing_fields:
            self.message = f"Perfil del usuario {user_id} incompleto. Campos faltantes: {', '.join(missing_fields)}"
        else:
            self.message = f"Perfil del usuario {user_id} está incompleto"
        super().__init__(self.message)

class UserDeletionNotAllowedException(AppBaseException):
    """Se lanza cuando no se puede eliminar un usuario por restricciones."""
    def __init__(self, user_id: int, reason: str = None):
        self.user_id = user_id
        self.reason = reason
        if reason:
            self.message = f"No se puede eliminar el usuario {user_id}. Razón: {reason}"
        else:
            self.message = f"No se puede eliminar el usuario {user_id}"
        super().__init__(self.message)
