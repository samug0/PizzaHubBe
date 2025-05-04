from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from pizza_hub_app.Domain.Controller.Cart.DTO.response.response import CartResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserAggregatedResponseDTO, UserResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.request.request import UpdateUserRequestDTO
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.models import User, Cart
import asyncio

logger = AppLogger(__name__)


class CartService(AbstractService):



    async def get_cart_by_user_id(self, id : UUID) -> dict:
        user : User = await self.repository_accessor.user_repository.get_by_id(id)
        cart : Cart = await asyncio.get_running_loop().run_in_executor(None, lambda: user.cart)
        aggregated_cart: dict= await self.repository_accessor.cart_repository.get_aggregated_cart(cart)
        return aggregated_cart