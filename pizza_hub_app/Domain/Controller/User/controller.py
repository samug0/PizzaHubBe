from typing import List, Mapping, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from pizza_hub_app.Domain.Controller.Auth.guard.auth_guard import AuthGuard
from pizza_hub_app.Domain.Controller.User.DTO.request.request import UpdateUserRequestDTO
from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserResponseDTO
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.utils.logger.logger import AppLogger

logger = AppLogger(__name__)


class UserController(AbstractController):
    def __init__(self):
        self.__router = APIRouter(prefix="/user", tags=["Users"])
        self.__user_service = UserService()
        self.configure_routes()

    def get_router(self):
        return self.__router

    def configure_routes(self):
        self.__router.get("", status_code=200, response_model=List[UserResponseDTO],  dependencies=[Depends(AuthGuard(['ADMIN']))])(self.get_all_users)
        self.__router.get("{id}", status_code=200, response_model=UserResponseDTO,  dependencies=[Depends(AuthGuard(['ADMIN', 'USER']))])(self.get_user_by_id)
        self.__router.patch("{id}", status_code=201, response_model=Mapping[str, bool], dependencies=[Depends(AuthGuard(['ADMIN', 'USER']))])(self.update_user_by_id)
        

    async def get_all_users(self):
        async def action():
            users: List[UserResponseDTO] = await self.__user_service.get_all_users()
            return users

        return await self.execute_action(action)
    

    async def get_user_by_id(self, id : UUID):
        async def action():
            user : Optional[UserResponseDTO] = await self.__user_service.get_user_by_id(id)
            return user
        
        return await self.execute_action(action)
    

    async def update_user_by_id(self, id : UUID, data : UpdateUserRequestDTO):
        async def action():
            response : bool = await self.__user_service.update_user_by_id(id, data)
            return self.success_response(response)
        
        return await self.execute_action(action)