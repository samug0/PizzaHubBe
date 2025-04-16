import os
from typing import List, Optional
from asgiref.sync import sync_to_async
from pizza_hub_app.models import Cart, CartProductInstance, ProductInstance, User, ProductInstanceIngredients

images_server_url = os.getenv("IMAGES_SERVER_URL", "http://localhost:8000/media/")

@sync_to_async
def convert_user_aggregated(user : User, cart_product_instance : List[ProductInstance], product_instance_ingredients : Optional[List[ProductInstanceIngredients]]) -> dict:

    # for  i in product_instance_ingredients:
    #     print(i.__dict__)
    cart_product_instances = [
        {
            "id": product_cart.id,
            "product_id":  product_cart.product.id,
            "total_price": product_cart.total_price,
            "created_at": product_cart.created_at,
            "updated_at": product_cart.updated_at
        }
        for product_cart in cart_product_instance
    ] if cart_product_instance is not None else []


    product_instance_ingredients = [
        {
            "id": product_instance_ingredient.id,
            "product_instance_id": product_instance_ingredient.product_instance.id,
            "ingredient_id": product_instance_ingredient.ingredient.id,
            "created_at": product_instance_ingredient.created_at,
            "updated_at": product_instance_ingredient.updated_at
        } for product_instance_ingredient in product_instance_ingredients
    ] if product_instance_ingredients is not None else []

    cart = {
        "id": user.cart.id,
        "created_at": user.cart.created_at,
        "updated_at": user.cart.updated_at,
        "product_instances": cart_product_instances
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