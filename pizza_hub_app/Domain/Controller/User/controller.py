from typing import List, Mapping
from uuid import UUID

from fastapi import APIRouter, Depends

from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserResponseDTO
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.models import User
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
        self.__router.get("", status_code=200, response_model=List[UserResponseDTO])(self.get_all_users)

    async def get_all_users(self):
        async def action():
            users: List[UserResponseDTO] = await self.__user_service.get_all_users()
            return users

        return await self.execute_action(action)