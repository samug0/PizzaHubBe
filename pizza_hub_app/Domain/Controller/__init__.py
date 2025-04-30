from fastapi import FastAPI

from pizza_hub_app.Domain.Controller.Category.controller import CategoryController
from pizza_hub_app.Domain.Controller.Product.controller import ProductController
from pizza_hub_app.Domain.Controller.User.controller import UserController
from pizza_hub_app.Domain.Controller.Auth.controller import AuthController
from pizza_hub_app.Domain.Controller.ProductInstance.controller import ProductInstanceController
from pizza_hub_app.Domain.Controller.Ingredient.controller import IngredientController
from pizza_hub_app.Domain.Controller.Cart.controller import CartController


def register_controllers(app: FastAPI):
    app.include_router(AuthController().get_router())
    app.include_router(UserController().get_router())
    app.include_router(ProductController().get_router())
    app.include_router(CategoryController().get_router())
    app.include_router(ProductInstanceController().get_router())
    app.include_router(IngredientController().get_router())
    app.include_router(CartController().get_router())