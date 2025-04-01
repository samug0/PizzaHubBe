from typing import Optional

from pydantic import EmailStr

from pizza_hub_app.models import User
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository


class UserRepository(GenericRepository[User]):

    async def get_by_email(self, email: EmailStr) -> Optional[User]:
        try:
            return await User.objects.aget(email=email)
        except User.DoesNotExist:
            return None

    async def get_by_username(self, username: str) -> Optional[User]:
        try:
            return await User.objects.aget(username=username)
        except User.DoesNotExist:
            return None
    
