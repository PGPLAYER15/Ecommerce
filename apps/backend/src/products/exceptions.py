from shared.exceptions import AppBaseException

class ProductNotFoundException(AppBaseException):
    """ Excepcion que se lanza cuando no se encuentra un producto"""
    def __init__(self, product_id: str):
        self.product_id = product_id
        self.message = f"Producto con ID '{product_id}' no encontrado"
        super().__init__(self.message)

class ProductNotFoundByNameException(AppBaseException):
    def __init__(self, product_name:str):
        self.product_name = product_name
        self.message = f"Producto con el nombre '{product_name}' no encontrado"
        super().__init__(self.message)

class DuplicateProductNameException(AppBaseException):
    """ Excepcion que se lanza cuando se encuentra un nombre de producto duplicado"""
    def __init__(self, product_name: str):
        self.product_name = product_name
        self.message = f"El nombre de producto '{product_name}' ya existe"
        super().__init__(self.message)

class InvalidProductPriceException(AppBaseException):
    """ Excepcion si el precio del producto es invalido"""
    def __init__(self, product_id: str, price: float):
        self.product_id = product_id
        self.price = price
        self.message = f"El precio '{price}' del producto con ID '{product_id}' es invalido"
        super().__init__(self.message)

class ProductOutOfStockException(AppBaseException):
    """ Excepcion que se lanza cuando un producto esta fuera de stock"""
    def __init__(self, product_id: str):
        self.product_id = product_id
        self.message = f"El producto con ID '{product_id}' esta fuera de stock"
        super().__init__(self.message)

class ProductIncompleteException(AppBaseException):
    """ Excepcion que se lanza cuando un producto esta incompleto"""
    def __init__(self, product_id: str):
        self.product_id = product_id
        self.message = f"El producto con ID '{product_id}' esta incompleto"
        super().__init__(self.message)