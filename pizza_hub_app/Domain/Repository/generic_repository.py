from typing import TypeVar, Generic, Type
from uuid import UUID

from pizza_hub_app.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        super().__init__()
        self.__model = model

    async def get_all(self):
        return [entity async for entity in self.__model.objects.all()]
    
    async def get_by_id(self, id: UUID):
        return await self.__model.objects.aget(pk=id)

    async def create(self, entity: dict):
        return await self.__model.objects.acreate(**entity)

    async def update(self, id: UUID, data: dict):
        existing_entity: T = await self.__model.objects.aget(pk=id)

        for key, value in data.items():
            setattr(existing_entity, key, value)

        await existing_entity.asave()
        return True

    async def delete(self, id: UUID):
        entity = await self.__model.objects.aget(pk=id)
        await entity.adelete()
        return True