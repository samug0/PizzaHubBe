import asyncio
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from pizza_hub_app.models import CartProductInstance, Ingredients, ProductInstance, ProductInstanceIngredients, User, Cart
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from fastapi.exceptions import HTTPException
from django.db.models import Q, Prefetch
from pizza_hub_app.Domain.Repository.User.assembler.assembler import convert_user_aggregated


prefetched_chart = Prefetch(('cart'), queryset=Cart.objects.all(), to_attr='cart_user')
prefetched_cart_product_instance = Prefetch(('cart_product_instance'), queryset=CartProductInstance.objects.filter(is_current=True), to_attr='cart_product_instances')
prefetched_product_instances = Prefetch(('product_instance'), queryset=ProductInstance.objects.all(), to_attr='product_instances')
prefetched_product_instances_ingredients = Prefetch(('product_instance_ingredients'), queryset=ProductInstanceIngredients.objects.all(), to_attr='product_instances_ingredients')
prefetched_related_ingredients = Prefetch(('ingredient'), queryset=Ingredients.objects.all(), to_attr='ingredients')

class UserRepository(GenericRepository[User]):

    async def get_user_aggregated_by_id(self, id : UUID):
        try:
            user_prefetched = await User.objects.prefetch_related(prefetched_chart).aget(pk=id)
            
            cart =  await asyncio.get_running_loop().run_in_executor(None, lambda: user_prefetched.cart)
            cart_product_instance_prefetched = await Cart.objects.prefetch_related(prefetched_cart_product_instance).aget(pk=cart.id)
            product_instances_ingredients_prefetched = []
            product_instances : List[ProductInstance] = []
            for i in cart_product_instance_prefetched.cart_product_instances:
                product_instance : ProductInstance = await asyncio.get_running_loop().run_in_executor(None, lambda: i.product_instance)
                product_instances.append(product_instance)

            for i in product_instances:
                product_instance_id = await asyncio.get_running_loop().run_in_executor(None, lambda: i.id)
                prefetched_product_instance : List[ProductInstance] = await ProductInstance.objects.prefetch_related(prefetched_product_instances_ingredients).aget(pk=product_instance_id)
                product_instances_ingredients_prefetched.append(prefetched_product_instance)
            user_aggregated = await convert_user_aggregated(user_prefetched, product_instances, product_instances_ingredients_prefetched)
          
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
        
        