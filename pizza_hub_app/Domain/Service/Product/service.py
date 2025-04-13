from typing import List, Optional
from pizza_hub_app.models import Product
from pizza_hub_app.Domain.Controller.Product.DTO.response.response import ProductResponseDTO
from pizza_hub_app.Domain.Service.abstract_service import AbstractService


class ProductService(AbstractService):

    async def getAll(self, name = Optional[str]) -> List[ProductResponseDTO]:
        products : List[Product] = await self.repository_accessor.product_repository.get_products_aggregated(name)
        return [ProductResponseDTO(**product) for product in products]
        # products_parsed : List = []
        # for i in products:
        #     product_parsed : Product = {"id": i.id, "name": i.name, "price": i.price,"description": i.description, "is_available": i.is_available, "created_at": i.created_at, "updated_at": i.updated_at}
        #     products_parsed.append(ProductResponseDTO(**product_parsed))
        # return products_parsed
    
    # async def getFilteredProductByName(self) -> List[Optional[ProductResponseDTO]]:
    #     products : List[Product] = await self.repository_accessor.product_repository.get_filtered_by_name()
    #     return [ProductResponseDTO(**product) for product in products]