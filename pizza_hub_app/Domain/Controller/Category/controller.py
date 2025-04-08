from typing import List
from fastapi import APIRouter
from pizza_hub_app.Domain.Controller.Category.DTO.response.response import CategoryResponseDTO
from pizza_hub_app.Domain.Service.Category.service import CategoryService
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController


class CategoryController(AbstractController):

    def __init__(self):
        self.__router = APIRouter(prefix="/category", tags=["Categorys"])
        self.__category_service = CategoryService()
        self.configure_routes()

    def get_router(self):
        return self.__router

    def configure_routes(self):
        self.__router.get("", status_code=200, response_model=List[CategoryResponseDTO])(self.get_all_categorys)

    
    async def get_all_categorys(self):
        async def action():
            categorys: List[CategoryResponseDTO] = await self.__category_service.get_all()
            return categorys

        return await self.execute_action(action)