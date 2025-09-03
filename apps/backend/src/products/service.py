from typing import Optional, List
from products.models import Product
from products.schemas import ProductCreate, ProductUpdate
from products.repository import ProductRepository
from products.exceptions import ProductNotFoundException, ProductNotFoundByNameException,DatabaseException
from shared.exceptions import InsufficientPermissionsException
import logging

class ProductService:
    
    def __init__(self,product_repo:ProductRepository) -> None:
        self.product_repo = product_repo
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, id: int) -> Product:

        if not isinstance(id, int) or id <= 0:
            raise ValueError("El ID del producto debe ser un entero positivo")
        product = await self.product_repo.get_by_id(id)
            
        if product is None:
            raise ProductNotFoundException(product_id=id)
            
        return product
    
    def get_by_name(self,name:str) -> Optional[Product]:
        product = self.product_repo.get_by_name(name)

        if product is None:
            raise ProductNotFoundByNameException(product_name=name)

        return product

    async def create_product(self, product_data: ProductCreate) -> Product:

        self.logger.info("Creando un nuevo producto")

        if product_data.price < 0:
            raise ValueError("El precio del producto debe ser un número positivo")

        if product_data.stock < 0:
            raise ValueError("El stock del producto debe ser un número positivo")

        try:
            existing_product = await self.get_by_name(product_data.name)
            if existing_product:
                raise ValueError("Ya existe un producto con ese nombre")

        except ProductNotFoundByNameException:
            pass
        
        product_model = Product(
            name = product_data.name,
            description = product_data.description,
            price = product_data.price,
            stock = product_data.stock
        )

        product = await self.product_repo.create(product_model)

        if product is None:
            raise DatabaseException("Fallo al intentar crear el producto")

        self.logger.info(f"Producto creado con ID: {product.id}")

        return product

    async def get_in_stock(self,skip:int = 0,limit:int = 10) -> List[Product]:
        
        if skip < 0:
            raise ValueError("El valor de 'skip' debe ser un número entero positivo")

        if limit <= 0 or limit > 100:
            raise ValueError("Limit debe estar entre 1 y 100")

        self.logger.info("Obteniendo productos que tienen stock")
        product = await self.product_repo.get_in_stock(skip,limit)
            
        if product is None:
            raise DatabaseException("Fallo al intentar cargar productos sin stock")

        self.logger.info(f"Se encontraron {len(product)} productos en stock")
        return product

    async def get_out_of_stock(self,skip:int = 0,limit:int = 10) -> List[Product]:
        
        if skip < 0:
            raise ValueError("El valor de 'skip' debe ser un número entero positivo")

        if limit <= 0 or limit > 100:
            raise ValueError("Limit debe estar entre 1 y 100")

        self.logger.info("Obteniendo productos que no tienen stock")
        product = await self.product_repo.get_out_of_stock(skip,limit)

        if product is None:
            raise DatabaseException("Fallo al intentar cargar productos sin stock")

        self.logger.info(f"Se encontraron {len(product)} productos sin stock")
        return product
    
    async def check_stock(self,product_id:int) -> bool:        
        stock = await self.product_repo.check_stock(product_id)

        return stock.stock > 0

    async def get_stock_quantity(self, product_id: int) -> int:
        return await self.product_repo.check_stock(product_id)

    async def low_stock(self,threshold:int = 5) -> List[Product]:
        
        if threshold < 0:
            raise ValueError("El threshold debe ser un número entero positivo")

        self.logger.info("Obteniendo productos con bajo stock")
        products = await self.product_repo.low_stock(threshold)

        if products is None:
            raise DatabaseException("Fallo al intentar cargar productos con bajo stock")

        self.logger.info(f"Se encontraron {len(products)} productos con bajo stock")
        return products

    async def update(self,product:Product, update_data: dict) -> Product:
        
        product = await self.get_by_id(product.id)
        
        update_dict = update_data.dict(exclude_unset=True)

        if 'price' in update_dict and update_dict['price'] < 0:
            raise ValueError("El precio no puede ser negativo")
        if 'stock' in update_dict and update_dict['stock'] < 0:
            raise ValueError("El stock no puede ser negativo")
        
        self.logger.info(f"Actualizando producto con ID: {product.id}")
        updated_product = await self.product_repo.update(product, update_dict)

        if updated_product is None:
            raise DatabaseException("Fallo al intentar actualizar el producto")

        self.logger.info(f"Producto con ID: {product.id} actualizado exitosamente")
        return updated_product
    
    async def update_stock(self, product_id: int, new_stock: int, user) -> Product:
        """Actualiza el stock de un producto (solo admins)."""
        if not user.is_admin:
            raise InsufficientPermissionsException()
        
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        product = await self.get_by_id(product_id)
        
        self.logger.info(f"Actualizando stock del producto con ID: {product.id}")
        updated_product = await self.product_repo.update_stock(product, new_stock)

        if updated_product is None:
            raise DatabaseException("Error al actualizar el stock del producto")

        self.logger.info(f"Stock del producto con ID: {product.id} actualizado exitosamente")
        return updated_product
    
    async def delete(self, product_id: int, user) -> None:
        """Elimina un producto (solo admins)."""
        if not user.is_admin:
            raise InsufficientPermissionsException()

        product = await self.get_by_id(product_id)
        
        self.logger.info(f"Eliminando producto con ID: {product.id}")
        result = await self.product_repo.delete(product)

        if not result:
            raise DatabaseException("Error al eliminar el producto")

        self.logger.info(f"Producto con ID: {product.id} eliminado exitosamente")

    async def list_products(self, skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[Product]:
        """Lista productos con paginación y búsqueda opcional."""
        if skip < 0:
            raise ValueError("Skip no puede ser negativo")
        if limit <= 0 or limit > 100:
            raise ValueError("Limit debe estar entre 1 y 100")
        
        return await self.product_repo.list_products(skip, limit, search)

    async def count_products(self, search: Optional[str] = None) -> int:
        """Cuenta el total de productos."""
        count = await self.product_repo.count_products(search)
        if count is None:
            raise DatabaseException("Error al contar los productos")
        return count

    async def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Obtiene productos en un rango de precios."""
        if min_price < 0 or max_price < 0:
            raise ValueError("Los precios no pueden ser negativos")
        if min_price > max_price:
            raise ValueError("El precio mínimo no puede ser mayor al máximo")

        return await self.product_repo.get_products_by_price_range(min_price, max_price)
