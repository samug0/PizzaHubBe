from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Request
from pizza_hub_app.Domain.Service.Ingredient.service import IngredientService
from pizza_hub_app.Domain.Controller.Ingredient.DTO.response import IngredientResponseDTO
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController


class IngredientController(AbstractController):
    def __init__(self):
        self.__router = APIRouter(prefix="/ingredient", tags=["Ingredients"])
        self.__ingredient_service = IngredientService()
        self.configure_routes()

    def get_router(self):
        return self.__router

    def configure_routes(self):
        self.__router.get("", status_code=200, response_model=List[IngredientResponseDTO])(self.get_all)
    

    async def get_all(self):
        async def action():
            ingredients: List[Optional[IngredientResponseDTO]] = await self.__ingredient_service.getAll()
            return ingredients

        return await self.execute_action(action)