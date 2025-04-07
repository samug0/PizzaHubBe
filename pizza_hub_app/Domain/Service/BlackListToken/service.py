from typing import Optional
from uuid import UUID
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.models import BlackListToken, User
from pizza_hub_app.utils.logger.logger import AppLogger
from datetime import datetime

logger = AppLogger(__name__)


class BlackListTokenService(AbstractService):

    
    async def get_user_by_token(self, token : str) -> Optional[User]:
        return await self.repository_accessor.black_list_token_repository.get_user_by_token(token)
    
    async def create(self, token : str, expires_at : int, user : User) -> bool:
        parsed_data : dict = {"token": token, "expires_at": datetime.fromtimestamp(expires_at / 1000), "user": user, "is_valid": True}
        created_black_list_token: BlackListToken = await self.repository_accessor.black_list_token_repository.create(parsed_data)
        if created_black_list_token:
            return True
        else:
            return False
        
    
    async def revoke_all_valid_user_token_by_user_id(self, user_id : UUID) -> bool:
        return await self.repository_accessor.black_list_token_repository.revoke_all_black_listed_token_by_user_id(user_id)
    
    