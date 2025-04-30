from typing import List, Optional
from uuid import UUID
from pizza_hub_app.Domain.Controller.ProductInstance.DTO.request.request import CreateProductInstanceRequestDTO
from pizza_hub_app.Domain.Service.Product.service import ProductService
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from django.core.exceptions import ObjectDoesNotExist


class ProductInstanceService(AbstractService):
  
  def __init__(self):
    super().__init__()

  async def create_product_instance(self, request : CreateProductInstanceRequestDTO)-> bool:
    validated_data : dict = CreateProductInstanceRequestDTO(**request.model_dump()).__dict__
    try:
      user = await self.repository_accessor.user_repository.get_by_id(validated_data.get('user_id'))
      product = await self.repository_accessor.product_repository.get_by_id(validated_data.get('product_id'))
      ingredients = []
      if validated_data.get('ingredients') is not None and len(validated_data.get('ingredients')) > 0:
        for i in validated_data.get('ingredients'):
          ingredient = await self.repository_accessor.ingredient_repository.get_by_id(i['id'])
          ingredients.append({"ingredient": ingredient, "quantity": i.get('quantity')})
        if user and product and ingredients:
          return await self.repository_accessor.product_instance_repository.create_and_associate_service_instance_to_cart(product, user, ingredients)
      else:
        if user and product:
          return await self.repository_accessor.product_instance_repository.create_and_associate_service_instance_to_cart(product, user)
    except ObjectDoesNotExist:
      raise ObjectDoesNotExist()