from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserAggregatedResponseDTO, UserResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.request.request import UpdateUserRequestDTO
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.models import User
from fastapi.exceptions import HTTPException

logger = AppLogger(__name__)


class UserService(AbstractService):



    async def get_all_users(self) -> List[UserResponseDTO]:
        users = await self.repository_accessor.user_repository.get_all()
        return [UserResponseDTO(**user.__dict__) for user in users]
    
    async def get_aggregated_user_by_id(self, id : UUID)-> Optional[UserAggregatedResponseDTO]:
        user = await self.repository_accessor.user_repository.get_user_aggregated_by_id(id)
        return UserAggregatedResponseDTO(**user)

    async def get_user_by_email(self, email : EmailStr) -> Optional[User]:
        return await self.repository_accessor.user_repository.get_by_email(email)
    
    
    async def get_user_by_username(self, username : str) -> Optional[User]:
        return await self.repository_accessor.user_repository.get_by_username(username)
    

    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        return await self.repository_accessor.user_repository.get_by_refresh_token(refresh_token)
    

    async def get_user_by_email_or_username(self, email_or_username : str) -> Optional[User]:
        return await self.repository_accessor.user_repository.get_user_by_email_or_username(email_or_username)
    

    async def get_user_by_id(self, id: UUID) -> Optional[User]:
        user : User = await self.repository_accessor.user_repository.get_by_id(id)
        if user:
            return UserResponseDTO(**user.__dict__)
        else:
            raise HTTPException(404, 'Not found')
        

    async def update_user_by_id(self, id: UUID, request : UpdateUserRequestDTO) -> bool:
        validated_data : dict = UpdateUserRequestDTO(**request.model_dump()).__dict__
        return await self.repository_accessor.user_repository.update(id, validated_data)

    
    
    
