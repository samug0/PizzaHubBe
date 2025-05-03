import json
import random
from typing import List, Optional
from uuid import UUID
import uuid

from pydantic import EmailStr

from pizza_hub_app.Domain.Controller.SumUp.DTO.request.request import CreatePaymentIntentRequestDTO
from pizza_hub_app.Domain.Controller.SumUp.DTO.response.response import CreatePaymentIntentResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserAggregatedResponseDTO, UserResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.request.request import UpdateUserRequestDTO
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.models import User
from fastapi.exceptions import HTTPException
import requests

logger = AppLogger(__name__)


class SumUpService(AbstractService):

    def __init__(self):
        super().__init__()
        self.__user_service = UserService()

    async def create_paymnet_intent(self, req : CreatePaymentIntentRequestDTO, merchant_code : str) -> CreatePaymentIntentResponseDTO:
        validated_data : dict = CreatePaymentIntentRequestDTO(**req.model_dump()).__dict__
        user = await self.__user_service.get_user_by_id(validated_data.get('user_id'))
        url_create_checkout = "https://api.sumup.com/v0.1/checkouts"
        headers : dict = {
            "Authorization": "Bearer sup_sk_MDJyKEl48k86t8FzdVWTzFZt0Gfkn1oWF",
            "Content-Type": "application/json"
        }
        reference = str(uuid.uuid4())
        data : dict = {
            "checkout_reference": reference,
            "merchant_code": merchant_code,
            "amount": 25.00,
            "currency": "EUR"
        }
        url_checkout_link = f"https://api.sumup.com/v0.1/checkouts/{reference}"

        response_checkout = requests.post(url_create_checkout, headers=headers, json=data)
        print(response_checkout.json())
        if response_checkout and response_checkout.status_code == 201:
            dict_response: dict = response_checkout.json()
            checkout_reference = dict_response.get('checkout_reference')

            # Costruisci manualmente l'URL del checkout
            payment_url = f"https://checkout.sumup.com/{checkout_reference}"

            print(f"Link per il pagamento: {payment_url}")