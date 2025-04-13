from typing import List, Optional
from fastapi import APIRouter, Request
from pizza_hub_app.Domain.Controller.Product.DTO.response.response import ProductResponseDTO
from pizza_hub_app.Domain.Service.Product.service import ProductService
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController


class ProductController(AbstractController):
    def __init__(self):
        self.__router = APIRouter(prefix="/product", tags=["Products"])
        self.__product_service = ProductService()
        self.configure_routes()

    def get_router(self):
        return self.__router

    def configure_routes(self):
        self.__router.get("", status_code=200, response_model=List[ProductResponseDTO])(self.get_all_products)
    

    async def get_all_products(self, name : str = ''):
        async def action():
            products: List[Optional[ProductResponseDTO]] = await self.__product_service.getAll(name)
            return products

        return await self.execute_action(action)


    # async def get_products_by_name(self):
    #     async def action():
    #         products_filtered : List[Optional[ProductResponseDTO]] = await self.__product_service.

    #     return await self.execute_action(action)