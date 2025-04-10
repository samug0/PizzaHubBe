"""
ASGI config for borgo_app_be project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza_hub.settings")
django.setup()

from fastapi.middleware.cors import CORSMiddleware

# configuration before mounting fastapi in django
# set app in django settings

from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from pizza_hub_app.Domain.Controller import register_controllers

django_app = get_asgi_application()

#fast_api_app = FastAPI(docs_url=None, redoc_url=None)
fast_api_app = FastAPI()
@fast_api_app.get(fast_api_app.root_path + "/openapi.json")
def custom_swagger_ui_html():
    return fast_api_app.openapi()

fast_api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init(app: FastAPI):
    register_controllers(app)
    app.mount("/django", django_app)
    # app.mount("/static", StaticFiles(directory="./static"))


init(fast_api_app)