from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class CreateProductInstanceRequestDTO(BaseModel):
    user_id : UUID
    product_id : UUID
    ingredients : Optional[List[UUID]] = None