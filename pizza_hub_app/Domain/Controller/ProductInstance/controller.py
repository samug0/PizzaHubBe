from functools import partial
from pizza_hub_app.Domain.Controller.Auth.guard.auth_guard import AuthGuard
from pizza_hub_app.Domain.Controller.ProductInstance.DTO.request.request import CreateProductInstanceRequestDTO
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from fastapi import APIRouter, Depends
from typing import Mapping
from pizza_hub_app.Domain.Service.ProductInstance.service import ProductInstanceService
from pizza_hub_app.utils.logger.logger import AppLogger


logger = AppLogger(__name__)



class ProductInstanceController(AbstractController):

    def __init__(self):
        self.__router = APIRouter(prefix="/product-instance", tags=["ProductInstance"])
        self.__product_instance_service = ProductInstanceService()
        self.configure_routes()

    def get_router(self):
        return self.__router


    def configure_routes(self):
        self.__router.post("", status_code=200, response_model=Mapping[str, bool])(self.create_product_instance)

    async def create_product_instance(self, request: CreateProductInstanceRequestDTO):
        async def action():
            response = await self.__product_instance_service.create_product_instance(request)
            if response == True:
                return self.success_response(True)
            else:
                return self.success_response(False)
        return await self.execute_action(action)


    