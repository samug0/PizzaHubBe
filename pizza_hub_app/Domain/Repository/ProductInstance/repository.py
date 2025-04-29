import asyncio
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from pizza_hub_app.models import Product, ProductInstance, User, CartProductInstance, ProductInstanceIngredients
from typing import List

class ProductInstanceRepository(GenericRepository[ProductInstance]):
    
    async def create_and_associate_service_instance_to_cart(self, product : Product, user : User, ingredients : List[dict] = None) -> bool:
        created_product_instance =await ProductInstance.objects.acreate(product=product, total_price=product.price)
        product_instance_ingredients = []
        for i in ingredients:
            for j in range(i.get('quantity')):
                product_instance_ingredient = ProductInstanceIngredients(product_instance=created_product_instance, ingredient=i.get('ingredient'))
                product_instance_ingredients.append(product_instance_ingredient)
        
        await ProductInstanceIngredients.objects.abulk_create(product_instance_ingredients)
        cart = await asyncio.get_running_loop().run_in_executor(None, lambda: user.cart)
        await CartProductInstance.objects.acreate(product_instance=created_product_instance, cart=cart)
        return True
