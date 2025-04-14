from typing import List, Optional
from uuid import UUID
from pizza_hub_app.Domain.Repository.generic_repository import GenericRepository
from pizza_hub_app.models import Product, ProductImages, ProductCategory, ProductIngredients
from django.db.models import Prefetch, Q
from pizza_hub_app.Domain.Repository.Product.assembler.assembler import convert_products_aggregated, convert_product_aggregated



# def prefetch_product_images():
#     """
#     Prefetch related images for products.
#     """
#     return Prefetch("images", queryset=ProductImages.objects.select_related("product"))


prefetched_images = Prefetch("product_images", queryset=ProductImages.objects.all(), to_attr="images")
prefetched_product_category = Prefetch("product_category", queryset=ProductCategory.objects.all(), to_attr="product_categories")
prefetched_product_ingredients = Prefetch("product_ingredients", queryset=ProductIngredients.objects.all(), to_attr="products_ingredients")

class ProductRepository(GenericRepository[Product]):




    async def get_products_aggregated(self, name = Optional[str])->List[dict]:
        """
        Get all products aggregated with their respective images and categories.
        """
        #products = await self.get_all()
        print(name)
        if(name and name != ''):
            products : List[Product] = [product async for product in Product.objects.prefetch_related(prefetched_images, prefetched_product_category, prefetched_product_ingredients).filter(name__startswith=name)]
            return await convert_products_aggregated(products)
        else:
            products : List[Product] = [product async for product in Product.objects.prefetch_related(prefetched_images, prefetched_product_category, prefetched_product_ingredients).all()]
            return await convert_products_aggregated(products)
    # async def get_filtered_by_name(self) -> List[dict]:
    #     products : List[Product] = [product async for product in Product.objects.filter(name__startswith=).values()]


    async def getById(self, id : UUID) -> Optional[dict]:
        product = await Product.objects.prefetch_related(prefetched_images, prefetched_product_category, prefetched_product_ingredients).aget(pk=id)
        return await convert_product_aggregated(product)
        