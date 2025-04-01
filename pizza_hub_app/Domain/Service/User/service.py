from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserResponseDTO
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.models import User

logger = AppLogger(__name__)


class UserService(AbstractService):


    async def get_all_users(self) -> List[UserResponseDTO]:
        users = await self.repository_accessor.user_repository.get_all()
        return [UserResponseDTO(**user.__dict__) for user in users]
    
    async def get_user_by_email(self, email : EmailStr) -> Optional[User]:
        return await self.repository_accessor.user_repository.get_by_email(email)
    
        
    
    async def get_user_by_username(self, username : str) -> Optional[User]:
        return await self.repository_accessor.user_repository.get_by_username(username)
    
    
