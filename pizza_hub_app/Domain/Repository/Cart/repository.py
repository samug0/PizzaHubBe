

from pizza_hub_app.Domain.Repository.Cart.assembler.assembler import convert_cart_aggregated
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from pizza_hub_app.models import Cart, CartProductInstance
from django.db.models import  Prefetch

prefetched_cart_product_instance = Prefetch(('cart_product_instance'), queryset=CartProductInstance.objects.filter(is_current=True), to_attr='cart_product_instances')

class CartRepository(GenericRepository[Cart]):
    
    async def get_aggregated_cart(self, cart : Cart) -> dict:
        cart_with_product_instances_prefetched = await Cart.objects.prefetch_related(prefetched_cart_product_instance).aget(pk=cart.id)
        return await convert_cart_aggregated(cart_with_product_instances_prefetched)