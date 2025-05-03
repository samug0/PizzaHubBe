from functools import partial

from fastapi.responses import JSONResponse
from pizza_hub_app.Domain.Controller.Auth.guard.auth_guard import AuthGuard
from pizza_hub_app.Domain.Controller.ProductInstance.DTO.request.request import CreateProductInstanceRequestDTO
from pizza_hub_app.Domain.Controller.SumUp.DTO.request.request import CreatePaymentIntentRequestDTO
from pizza_hub_app.Domain.Controller.SumUp.DTO.response.response import CreatePaymentIntentResponseDTO
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from fastapi import APIRouter, Depends
from typing import Mapping
from pizza_hub_app.Domain.Service.ProductInstance.service import ProductInstanceService
from pizza_hub_app.Domain.Service.SumUp.service import SumUpService
from pizza_hub_app.utils.logger.logger import AppLogger
from sumup import Sumup # type: ignore

logger = AppLogger(__name__)



class SumUpController(AbstractController):

    def __init__(self):
        self.__router = APIRouter(prefix="/sum-up", tags=["SumUp"])
        self.__client = Sumup(api_key='sup_sk_MDJyKEl48k86t8FzdVWTzFZt0Gfkn1oWF')
        self.__sum_up_service = SumUpService()
        self.configure_routes()

    def get_router(self):
        return self.__router


    def configure_routes(self):
        self.__router.post("/create-payment-intent", status_code=200, response_model=CreatePaymentIntentResponseDTO)(self.create_payment_intent)

    async def create_payment_intent(self, request: CreatePaymentIntentRequestDTO):
        async def action():
            client = self.__client.merchant.get()
            dict_client: dict = client.__dict__
            merchant_code : str = dict_client.get('merchant_profile').__dict__.get('merchant_code')
            client_secret_id: str = await self.__sum_up_service.create_paymnet_intent(request, merchant_code)
            if client_secret_id:
                return JSONResponse(content=client_secret_id)
            else:
                return self.success_response(False)
        return await self.execute_action(action)