from pizza_hub_app.Domain.Repository.User.repository import UserRepository, User
from pizza_hub_app.Domain.Repository.BlackList.repository import BalckListTokenRepository, BlackListToken


class RepositoryAccessor:
    def __init__(self):
        self.user_repository = UserRepository(model=User)
        self.black_list_token_repository = BalckListTokenRepository(model=BlackListToken)