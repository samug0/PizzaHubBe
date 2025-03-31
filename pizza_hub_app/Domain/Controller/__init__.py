from fastapi import FastAPI

from pizza_hub_app.Domain.Controller.User.controller import UserController

def register_controllers(app: FastAPI):
    app.include_router(UserController().get_router())