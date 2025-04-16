import os
from typing import List, Optional
from asgiref.sync import sync_to_async
from pizza_hub_app.models import Cart, CartProductInstance, ProductInstance, User, ProductInstanceIngredients
from django.db.models import Prefetch

images_server_url = os.getenv("IMAGES_SERVER_URL", "http://localhost:8000/media/")

@sync_to_async
def convert_user_aggregated(user : User, cart_product_instance : List[ProductInstance], product_instance_ingredients : Optional[List[ProductInstanceIngredients]]) -> dict:
    #prefetched_ingredients =
    cart_product_instances = []
            
    for product_cart in cart_product_instance:
        product_instance: dict = {
            "id": product_cart.id,
            "product_id": product_cart.product.id,
            "product_price": product_cart.product.price,
            "product_name":  product_cart.product.name,
            "total_price": product_cart.total_price,
            "created_at": product_cart.created_at,
            "updated_at": product_cart.updated_at
        }
        ingredients_list = []
        if len(product_instance_ingredients) > 0:
            for i in product_instance_ingredients:
                #print(i.product_instances_ingredients)
                print(i.product_instance)
                for j in i.product_instances_ingredients:
                    ingredient = {
                        "id": j.ingredient.id,
                        "name": j.ingredient.name,
                        "price": j.ingredient.price,
                    }
                    ingredients_list.append(ingredient)
        product_instance.update({"ingredients": ingredients_list})        
        cart_product_instances.append(product_instance)

    cart = {
        "id": user.cart.id,
        "created_at": user.cart.created_at,
        "updated_at": user.cart.updated_at,
        "product_instances": cart_product_instances,
        "quantity": len(cart_product_instance)
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