from abc import ABC , abstractmethod
from auth.models import User
from typing import Optional

class UserAuthInterface(ABC):

    @abstractmethod
    def create_user(self, user:User) -> User:
        pass

    @abstractmethod
    def existing_user(self,user:User) -> bool:
        pass