from fastapi import FastAPI

from pizza_hub_app.Domain.Controller.User.controller import UserController
from pizza_hub_app.Domain.Controller.Auth.controller import AuthController

def register_controllers(app: FastAPI):
    app.include_router(AuthController().get_router())
    app.include_router(UserController().get_router())