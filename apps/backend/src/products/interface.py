from abc import ABC, abstractmethod
from products.models import Product
from typing import Optional, List

class ProductInterface(ABC):

    @abstractmethod
    async def get_by_id(self,id:int) -> Optional[Product]:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def list(self) -> List[Product]:
        pass