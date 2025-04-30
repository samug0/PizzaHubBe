from typing import List, Mapping, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pizza_hub_app.Domain.Service.Cart.service import CartService
from pizza_hub_app.Domain.Controller.Cart.DTO.response.response import CartResponseDTO
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from pizza_hub_app.utils.logger.logger import AppLogger

logger = AppLogger(__name__)


class CartController(AbstractController):
    def __init__(self):
        self.__router = APIRouter(prefix="/cart", tags=["Cart"])
        self.__cart_service = CartService()
        self.configure_routes()

    def get_router(self):
        return self.__router

    def configure_routes(self):
        self.__router.get("/user/{id}", status_code=200, response_model=CartResponseDTO)(self.get_cart_by_user_id)
        

    async def get_cart_by_user_id(self, id : UUID):
        async def action():
            cart : CartResponseDTO = await self.__cart_service.get_cart_by_user_id(id)
            return cart

        return await self.execute_action(action)