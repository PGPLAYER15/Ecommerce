from abc import ABC , abstractmethod
from auth.models import User
from typing import Optional

class UserInterface(ABC):
    
    @abstractmethod
    async def get_by_email(self,email:str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id:int) -> Optional[User]:
        pass
    @abstractmethod
    async def update_user(self,user_data:User,update_data:dict) -> User:
        pass