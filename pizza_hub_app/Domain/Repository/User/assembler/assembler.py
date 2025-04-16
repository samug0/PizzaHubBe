import os
from asgiref.sync import sync_to_async
from pizza_hub_app.models import User

images_server_url = os.getenv("IMAGES_SERVER_URL", "http://localhost:8000/media/")

@sync_to_async
def convert_user_aggregated(user : User) -> dict:
    cart = {
        "id": user.cart.id,
        "created_at": user.cart.created_at,
        "updated_at": user.cart.updated_at
    }

    return {
        "id": user.id,
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
        "phone_number": user.phone_number,
        "address": user.address,
        "city": user.city,
        "country": user.country,
        "profile_image": images_server_url,
        "role": user.role.name,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "cart": cart
    }