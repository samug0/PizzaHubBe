from abc import ABC
from pizza_hub_app.Domain.Repository import RepositoryAccessor


class AbstractService(ABC):
    def __init__(self):
        super().__init__()
        self.repository_accessor = RepositoryAccessor()