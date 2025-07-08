from abc import ABC , abstractmethod
from auth.models import User
from typing import Optional

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_email(self,email:str) -> Optional[User]:
        pass
    
    @abstractmethod
    def create(self, user:User) -> User:
        pass

    @abstractmethod
    def existing_user(self,user:User) -> bool:
        pass