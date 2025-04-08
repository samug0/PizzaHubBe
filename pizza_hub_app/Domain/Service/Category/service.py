from typing import List

from pizza_hub_app.Domain.Controller.Category.DTO.response.response import CategoryResponseDTO
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.models import Category


class CategoryService(AbstractService):


    async def get_all(self) -> List[CategoryResponseDTO]:
        categorys : List[Category] = await self.repository_accessor.category_repository.get_all()
        categotys_parsed : List = []
        for i in categorys:
            category_parsed : Category = {"id": i.id, "name": i.name, "price": i.desription, "created_at": i.created_at, "updated_at": i.updated_at}
            categotys_parsed.append(CategoryResponseDTO(**category_parsed))
        return categotys_parsed
