import os
from typing import List
from pizza_hub_app.models import Product, ProductImages
from asgiref.sync import sync_to_async


images_server_url = os.getenv("IMAGES_SERVER_URL", "http://localhost:8000/media/")


@sync_to_async
def convert_product_aggregated(product : Product):
    """
    Convert a product to a dictionary with its aggregated data.
    """
    product_images = [
            {
                "id": image.id,
                "image": images_server_url + str(image.image)
            }
            for image in product.images
        ] if product.images is not None else []
    

    product_category = [
        {
            "id": category.category.id,
            "name": category.category.name,
            "description": category.category.description,
        } for category in product.product_categories
    ] if len(product.product_categories) > 0 else []


    product_ingredients = [
        {
            "id": ingredient.ingredient.id,
            "name": ingredient.ingredient.name,
            "description": ingredient.ingredient.description,
            "price": ingredient.ingredient.price,
            "is_available": ingredient.ingredient.is_available,
        } for ingredient in product.products_ingredients
    ] if len(product.products_ingredients) > 0 else []

    
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "is_available": product.is_available,
        "images": product_images,
        "ingredients": product_ingredients,
        "product_categories": product_category,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }



async def convert_products_aggregated(products: List[Product]):
    return [await convert_product_aggregated(product) for product in products]