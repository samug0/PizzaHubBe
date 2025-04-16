from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from pizza_hub_app.models import CartProductInstance, User, Cart
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from fastapi.exceptions import HTTPException
from django.db.models import Q, Prefetch
from pizza_hub_app.Domain.Repository.User.assembler.assembler import convert_user_aggregated


prefetched_chart = Prefetch(('cart'), queryset=Cart.objects.all(), to_attr='cart_user')
prefetched_cart_product_instance = Prefetch(('cart_product_instance'), queryset=CartProductInstance.objects.all(), to_attr='cart_product_instances')

class UserRepository(GenericRepository[User]):

    async def get_user_aggregated_by_id(self, id : UUID):
        try:
            user_prefetched = await User.objects.prefetch_related(prefetched_chart).aget(pk=id)
            print(user_prefetched.cart.id)
            cart_product_instance_prefetched = [i async for i in CartProductInstance.objects.filter(cart=user_prefetched.cart.id)]
            print(cart_product_instance_prefetched)
            user_aggregated = await convert_user_aggregated(user_prefetched)
            print(user_aggregated)
            return user_aggregated
        except User.DoesNotExist:
            return None
        
    async def get_by_email(self, email: EmailStr) -> Optional[User]:
        try:
            return await User.objects.aget(email=email)
        except User.DoesNotExist:
            return None

    async def get_by_username(self, username: str) -> Optional[User]:
        try:
            return await User.objects.aget(username=username)
        except User.DoesNotExist:
            return None
        
    
    async def get_by_refresh_token(self, refresh_token: str)-> Optional[User]:
        try:
            return await User.objects.aget(refresh_token=refresh_token)
        except User.DoesNotExist:
            raise HTTPException(401, 'Unauthorized')
    

    async def get_user_by_email_or_username(self, username_or_email: str) -> Optional[User]:
        try:
            return await User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).afirst()
        except User.DoesNotExist:
            return None
        
        