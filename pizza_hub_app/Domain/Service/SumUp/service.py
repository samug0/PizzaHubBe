import json
import random
from typing import List, Optional
from uuid import UUID
import uuid

from fastapi import HTTPException
from pydantic import EmailStr

from pizza_hub_app.models import Order, OrderStatus
from pizza_hub_app.Domain.Service.Cart.service import CartService
from pizza_hub_app.Domain.Controller.SumUp.DTO.request.request import CreatePaymentIntentRequestDTO
from pizza_hub_app.Domain.Controller.SumUp.DTO.response.response import CreatePaymentIntentResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.response.response import UserAggregatedResponseDTO, UserResponseDTO
from pizza_hub_app.Domain.Controller.User.DTO.request.request import UpdateUserRequestDTO
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.utils.logger.logger import AppLogger
import requests
from datetime import datetime, timedelta, timezone

logger = AppLogger(__name__)


class SumUpService(AbstractService):

    def __init__(self):
        super().__init__()
        self.__user_service = UserService()
        self.__cart_service = CartService()

    async def create_paymnet_intent(self, req : CreatePaymentIntentRequestDTO, merchant_code : str) -> CreatePaymentIntentResponseDTO:
        validated_data : dict = CreatePaymentIntentRequestDTO(**req.model_dump()).__dict__
        user = await self.__user_service.get_user_by_id(validated_data.get('user_id'))
        url_create_checkout = "https://api.sumup.com/v0.1/checkouts"
        headers : dict = {
            "Authorization": "Bearer sup_sk_MDJyKEl48k86t8FzdVWTzFZt0Gfkn1oWF",
            "Content-Type": "application/json"
        }
        reference = str(uuid.uuid4())
        cart_user = await self.__cart_service.get_cart_by_user_id(user.id)
        product_instances = cart_user.get('product_instances')
        #print('Count totale degli item', len(product_instances))
        updated_dict_product = []
        for i in product_instances:
            del i['id']
            if i not in updated_dict_product:
                updated_dict_product.append(i)
        
        now = datetime.now(timezone.utc)
        future_time = now + timedelta(minutes=5)
        iso_string = future_time.replace(microsecond=0).isoformat()
        data : dict = {
            "checkout_reference": str(user.id),
            "merchant_code": merchant_code,
            "amount": cart_user.get('total'),
            #"amount": 0.10,
            "currency": "EUR",
            "hosted_checkout": { "enabled": True },
            "return_url": "http://localhost:8001/sum-up/validate/checkout/payment",
            #"customer_id": str(user.id),
            "description": f'Quantità : {len(product_instances)}',
            "valid_until": iso_string
        }
        response_checkout = requests.post(url_create_checkout, headers=headers, json=data)
        print(response_checkout.json())
        if response_checkout and response_checkout.status_code == 201:
            dict_response: dict = response_checkout.json()
            #print(dict_response)
            checkout_url: str = dict_response.get('hosted_checkout_url')
            return CreatePaymentIntentResponseDTO(**{"payment_url": checkout_url})
    

    async def validate_checkout_payment(self, payload_signature : str) -> bool:
        print('ciaop')
    


    async def get_payment_status_by_transaction_id(self, id : UUID) -> bool:
        url: str = f'https://api.sumup.com/v0.1/checkouts/{id}'
        headers : dict = {
            "Authorization": "Bearer sup_sk_MDJyKEl48k86t8FzdVWTzFZt0Gfkn1oWF",
            "Content-Type": "application/json"
        }
        response_get_checkout = requests.get(url, headers=headers)
        if response_get_checkout.status_code == 200:
            response_dict: dict = response_get_checkout.json()
            if response_dict.get('status') == 'PAID' or response_dict.get('status') == 'SUCCESSFULL':
                user = await self.__user_service.get_user_by_id(response_dict.get('checkout_reference'))
                data_order : dict = {
                    "user": user,
                    "total": response_dict.get('amount'),
                    "approved": True,
                    "status": OrderStatus.APPROVED,
                    "is_payed": True
                }
                await Order.objects.acreate(data_order)
                return True
                
        elif response_get_checkout.status_code == 404:
            raise HTTPException(404, 'Not found')
        else:
            raise HTTPException(400, 'An Error occured in process of checkout')