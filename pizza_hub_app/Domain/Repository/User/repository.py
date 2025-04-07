from typing import Optional

from pydantic import EmailStr

from pizza_hub_app.models import User
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from fastapi.exceptions import HTTPException
from django.db.models import Q

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
        
    
    async def get_by_refresh_token(self, refresh_token: str)-> Optional[User]:
        try:
            return await User.objects.aget(refresh_token=refresh_token)
        except User.DoesNotExist:
            raise HTTPException(401, 'Unauthorized')
    

    async def get_user_by_email_or_username(self, username_or_email: str) -> Optional[User]:
        try:
            return await User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).afirst()
        except User.DoesNotExist:
            return None
        
        