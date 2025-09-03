class AppBaseException(Exception):
    """Excepción base para toda la aplicación."""
    pass

class UserNotFoundException(AppBaseException):
    """Se lanza cuando no se encuentra un usuario."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"Usuario con ID {user_id} no encontrado"
        super().__init__(self.message)

class DatabaseException(AppBaseException):
    """Error general de base de datos."""
    def __init__(self, detail: str = "Error en la base de datos"):
        self.message = detail
        super().__init__(self.message)

class InsufficientPermissionsException(AppBaseException):
    """Se lanza cuando el usuario no tiene permisos suficientes."""
    def __init__(self, user_id: int, required_permission: str = None):
        self.user_id = user_id
        self.required_permission = required_permission
        if required_permission:
            self.message = f"Usuario con ID {user_id} no tiene permisos para: {required_permission}"
        else:
            self.message = f"Usuario con ID {user_id} no tiene permisos suficientes"
        super().__init__(self.message)