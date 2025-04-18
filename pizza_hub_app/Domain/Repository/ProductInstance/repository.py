import asyncio
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from pizza_hub_app.models import Product, ProductInstance, User, CartProductInstance

class ProductInstanceRepository(GenericRepository[ProductInstance]):
    
    async def create_and_associate_service_instance_to_cart(self, product : Product, user : User) -> bool:
        created_product_instance =await ProductInstance.objects.acreate(product=product, total_price=product.price)
        print(created_product_instance)
        cart = await asyncio.get_running_loop().run_in_executor(None, lambda: user.cart)
        await CartProductInstance.objects.acreate(product_instance=created_product_instance, cart=cart)
        return True
