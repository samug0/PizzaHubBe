from pizza_hub_app.Domain.Repository.Category.repository import CategoryRepository, Category
from pizza_hub_app.Domain.Repository.Product.repository import ProductRepository, Product
from pizza_hub_app.Domain.Repository.User.repository import UserRepository, User
from pizza_hub_app.Domain.Repository.BlackList.repository import BlackListTokenRepository, BlackListToken


class RepositoryAccessor:
    def __init__(self):
        self.user_repository = UserRepository(model=User)
        self.black_list_token_repository = BlackListTokenRepository(model=BlackListToken)
        self.product_repository = ProductRepository(model=Product)
        self.category_repository = CategoryRepository(model=Category)