from products.interface import ProductInterface
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from products.models import Product
from shared.exceptions import DatabaseException
from typing import Optional, List
import logging 

logger = logging.getLogger(__name__)

class ProductRepository(ProductInterface):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_id(self,id:int)-> Optional[Product]:
        """
            Obtiene un producto con su id.
            
            Args:
                id (int): ID del producto.

            Returns:
                Optional[Product]: El producto encontrado o None si no existe.
        """
        try:
            logger.info(f"Buscando producto con ID: {id}")
            product = self.db.query(Product).filter(Product.id == id).first()
            
            if product:
                logger.debug(f"Producto encontrado exitosamente: {product.id}")
            else:
                logger.debug(f"No se encontró ningún producto con ID: {id}")
            return product
        except IntegrityError as e:
            logger.error(f"Error de integridad buscando producto por su ID {id}: {str(e)}")
            raise DatabaseException("Error al buscar producto en la base de datos") from e
        except SQLAlchemyError as e:
            logger.error(f"Error de BD buscando producto por su ID {id}: {str(e)}")
            raise DatabaseException("Error al buscar producto en la base de datos") from e
        
    async def get_by_name(self,name:str) -> Optional[Product]:
        """
            Obtiene un producto por nombre
            
            Args:
                name(str): El nombre del producto que se va a buscar.

            Returns:
                Optional[Product]: El producto encontrado o None si no existe.
        """
        try:
            logger.info(f"Buscando producto con nombre: {name}")
            product = self.db.query(Product).filter(
                func.lower(Product.name) == func.lower(name)
            ).first()
            
            if product:
                logger.debug(f"Producto encontrado exitosamente: {product.name}")
            else:
                logger.debug(f"No se encontró ningún producto con nombre: {name}")
                
            return product
        except IntegrityError as e:
            logger.error(f"Error de integridad buscando producto por nombre {name}: {str(e)}")
            raise DatabaseException("Error al buscar producto en la base de datos") from e
        except SQLAlchemyError as e:
            logger.error(f"Error de BD buscando producto por nombre {name}: {str(e)}")
            raise DatabaseException("Error al buscar producto en la base de datos") from e
    
    async def get_in_stock(self,skip:int = 0,limit:int = 10)-> List[Product]:
        try:
            logger.info("Obteniendo productos que tienen stock")
            products = (self.db.query(Product)
                        .filter(Product.stock > 0)
                        .offset(skip)
                        .limit(limit)
                        .all())

            logger.debug(f"Productos en stock obtenidos: {len(products)} productos")

            return products
        except IntegrityError as e:
            logger.error(f"Error de integridad al obtener productos en stock: {str(e)}")
            raise DatabaseException("Error al obtener productos en stock") from e
        except SQLAlchemyError as e:
            logger.error(f"Error de BD al obtener productos en stock: {str(e)}")
            raise DatabaseException("Error al obtener productos en stock") from e
    
    async def get_out_of_stock(self,skip:int = 0, limit:int = 10)-> List[Product]:
        try:
            logger.info("Obteniendo productos que no tienen stock")
            products = (self.db.query(Product)
                        .filter(Product.stock == 0)
                        .offset(skip)
                        .limit(limit)
                        .all())
            
            logger.debug(f"Productos sin stock obtenidos: {len(products)} productos")
            return products

        except IntegrityError as e:
            logger.error(f"Error de integridad al obtener productos sin stock: {str(e)}")
            raise DatabaseException("Error al obtener productos sin stock") from e
        except SQLAlchemyError as e:
            raise DatabaseException("Error al obtener productos sin de estock") from e
    
    async def check_stock(self,product_id:int) -> int:
        
        """
            Checa si hay stock del producto por medio del id.
            
            Args:
                product_id(int): id del producto que queremos checar su stock
            
            Returns:
                int: Devuelve la cantidad de stock que tiene un producto.
            
            Raise:
                DatabaseException: Si ocurre un error al consultar el stock del producto.
        """
        
        try:
            logger.info(f"Consultando stock del producto ID: {product_id}")
            stock = self.db.query(Product.stock).filter(Product.id == product_id).scalar()
            
            if stock is None:
                raise DatabaseException(f"Producto con ID {product_id} no encontrado")
                
            logger.debug(f"Stock del producto {product_id}: {stock}")
            return stock
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad consultando stock del producto {product_id}: {str(e)}")
            raise DatabaseException("Error al consultar stock del producto en la base de datos") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de BD consultando stock del producto {product_id}: {str(e)}")
            raise DatabaseException("Error al consultar stock del producto en la base de datos") from e
    
    async def low_stock(self,threshold:int) -> List[Product]:
        try:
            products = (self.db.query(Product)
                        .filter(Product.stock < threshold)
                        .filter(Product.stock > 0)  # Excluir productos sin stock
                        .all())
            logger.debug(f"Productos con stock bajo encontrados: {len(products)}")
            return products
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad consultando productos con stock bajo: {str(e)}")
            raise DatabaseException("Error al consultar productos con stock bajo en la base de datos") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de BD consultando productos con stock bajo: {str(e)}")
            raise DatabaseException("Error al consultar productos con stock bajo en la base de datos") from e

    async def create(self, product_data: Product) -> Product:
        """
            Crea un producto
            
            Args:
                product_data(Product): Recibe un objeto del producto
            Returns:
                Product: El producto creado
            Raises:
                DatabaseException: Si ocurre un error al crear el producto.
        """
        try: 
            
            self.db.add(product_data)
            self.db.commit()
            self.db.refresh(product_data)
            logger.info(f"Producto creado exitosamente: {product_data.id}")
            return product_data 
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear producto: {str(e)}")
            self.db.rollback()
            raise DatabaseException("Error al crear producto en la base de datos") from e
        except SQLAlchemyError as e:
            logger.error(f"Error de BD al crear producto: {str(e)}")
            self.db.rollback()
            raise DatabaseException("Error al crear producto en la base de datos") from e

    async def update(self, product: Product, update_data: dict) -> Product:
        """
            Actualiza un producto existente.

            Args:
                product (Product): El producto a actualizar.
                update_data (dict): Un diccionario con los campos a actualizar.

            Returns:
                Product: El producto actualizado.

            Raises:
                DatabaseException: Si ocurre un error al actualizar el producto.
        """
        try:
            for field, value in update_data.items():
                if hasattr(product, field) and value is not None:
                    old_value = getattr(product, field)
                    setattr(product, field, value)
                    logger.debug(f"Campo {field} actualizado: {old_value} -> {value}")
            self.db.commit()
            self.db.refresh(product)
            
            logger.info(f"Producto actualizado exitosamente: {product.id}")
            return product
        
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad actualizando producto {product.id}: {str(e)}")
            raise DatabaseException("Error al actualizar producto en la base de datos") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de BD actualizando producto {product.id}: {str(e)}")
            raise DatabaseException("Error al actualizar producto en la base de datos") from e
    
    async def update_stock(self,product:Product,stock:int) -> Product:
        
        """
            Actualiza el stock del producto.
            Args:
                product (Product): El producto a actualizar.
                stock (int): El nuevo stock del producto.

            Returns:
                Product: El producto actualizado.

            Raises:
                DatabaseException: Si ocurre un error al actualizar el stock del producto.
        """
        
        try:
            logger.info(f"Actualizando stock del producto ID: {product.id}")
            old_stock = product.stock
            product.stock = stock
            
            self.db.commit()
            self.db.refresh(product)
            
            logger.info(f"Stock actualizado exitosamente: {old_stock} -> {stock}")
            return product
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad actualizando stock del producto {product.id}: {str(e)}")
            raise DatabaseException("Error al actualizar stock del producto en la base de datos") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de BD actualizando stock del producto {product.id}: {str(e)}")
            raise DatabaseException("Error al actualizar stock del producto en la base de datos") from e    



    async def delete(self, product: Product) -> bool:
        """
            Elimina un producto de la base de datos.

            Args:
                product(Product): El producto a eliminar.

            Returns:
                bool: True si se elimina exitosamente. False si no es asi.
        """
        try:
            logger.info(f"Eliminando producto ID: {product.id}")
            product_id = product.id  # Guardar ID para logging
            
            self.db.delete(product)
            self.db.commit()
            
            logger.info(f"Producto eliminado exitosamente: {product_id}")
            return True
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Error de integridad eliminando producto {product.id}: {str(e)}")
            raise DatabaseException("Error al eliminar producto en la base de datos") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de BD eliminando producto {product.id}: {str(e)}")
            raise DatabaseException("Error al eliminar producto en la base de datos") from e

    def list_products(self, skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[Product]:
        """
            Da una lista de productos.
            
            Args:
                skip (int): El número de productos a omitir.
                limit (int): El número máximo de productos a devolver.
                search (Optional[str]): Una cadena de búsqueda para filtrar productos por nombre.

            Returns:
                List[Product]: Una lista de productos.
            
            Raise:
                DatabaseException: Si ocurre un error al listar los productos.
        """
        try:
            logger.info(f"Listando productos - skip: {skip}, limit: {limit}, search: {search}")
            query = self.db.query(Product)

            if search:
                search_term = f"%{search.strip()}%"
                query = query.filter(Product.name.ilike(search_term))
                
            products = query.offset(skip).limit(limit).all()
            logger.debug(f"Productos encontrados: {len(products)}")

            return products
        except SQLAlchemyError as e:
            logger.error(f"Error de BD listando productos: {str(e)}")
            raise DatabaseException("Error al listar productos en la base de datos") from e

    def count_products(self, search: Optional[str] = None) -> int:
        """
            Cuenta el número de productos en la base de datos.

            Args:
                search (Optional[str]): Una cadena de búsqueda para filtrar productos por nombre.

            Returns:
                int: El número de productos.

            Raises:
                DatabaseException: Si ocurre un error al contar los productos.
        """
        try:
            logger.info(f"Contando productos - search: {search}")
            query = self.db.query(Product)

            if search:
                search_term = f"%{search.strip()}%"
                query = query.filter(Product.name.ilike(search_term))

            count = query.count()
            logger.debug(f"Total de productos encontrados: {count}")

            return count
        except SQLAlchemyError as e:
            logger.error(f"Error de BD contando productos: {str(e)}")
            raise DatabaseException("Error al contar productos en la base de datos") from e
    
    async def get_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Obtiene productos en un rango de precios específico."""
        try:
            logger.info(f"Buscando productos en rango de precio: {min_price} - {max_price}")
            products = (self.db.query(Product)
                        .filter(Product.price >= min_price)
                        .filter(Product.price <= max_price)
                        .all())
            
            logger.debug(f"Productos en rango de precio encontrados: {len(products)}")
            return products
            
        except SQLAlchemyError as e:
            logger.error(f"Error de BD buscando productos por rango de precio: {str(e)}")
            raise DatabaseException("Error al buscar productos por rango de precio") from e

    async def get_most_expensive(self, limit: int = 10) -> List[Product]:
        """Obtiene los productos más caros."""
        try:
            logger.info(f"Obteniendo los {limit} productos más caros")
            products = (self.db.query(Product)
                        .order_by(Product.price.desc())
                        .limit(limit)
                        .all())
            
            logger.debug(f"Productos más caros encontrados: {len(products)}")
            return products
            
        except SQLAlchemyError as e:
            logger.error(f"Error de BD obteniendo productos más caros: {str(e)}")
            raise DatabaseException("Error al obtener productos más caros") from e