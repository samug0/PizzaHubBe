from pizza_hub_app.Domain.Repository.User.repository import UserRepository, User

class RepositoryAccessor:
    def __init__(self):
        self.user_repository = UserRepository(model=User)