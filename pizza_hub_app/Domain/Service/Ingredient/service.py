from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from pizza_hub_app.Domain.Controller.Ingredient.DTO.response import IngredientResponseDTO
from pizza_hub_app.models import Ingredients
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from django.core.exceptions import ObjectDoesNotExist


class IngredientService(AbstractService):

    async def getAll(self) -> List[IngredientResponseDTO]:
        ingredients : List[Ingredients] = await self.repository_accessor.ingredient_repository.get_all()
        return [IngredientResponseDTO(**ingredient.__dict__) for ingredient in ingredients]