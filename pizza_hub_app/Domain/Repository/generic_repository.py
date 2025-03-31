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