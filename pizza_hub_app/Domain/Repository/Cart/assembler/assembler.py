from asgiref.sync import sync_to_async
from pizza_hub_app.models import Cart, ProductInstanceIngredients, ProductInstance
from django.db.models import Prefetch


prefetched_product_instances_ingredients = Prefetch(('product_instance_ingredients'), queryset=ProductInstanceIngredients.objects.all(), to_attr='product_instances_ingredients')

@sync_to_async
def convert_cart_aggregated(cart : Cart)-> dict:
    total: float = 0.0
    product_instances = []

    for i in cart.cart_product_instances:
        # Prefetch ingredienti per ogni product_instance
        prefetched_data = ProductInstance.objects.prefetch_related(prefetched_product_instances_ingredients).get(pk=i.product_instance.id)

        ingredients = []
        for j in prefetched_data.product_instances_ingredients:
            ingredient = {
                "id": j.ingredient.id,
                "name": j.ingredient.name,
                "price": j.ingredient.price,
            }
            ingredients.append(ingredient)
            total += j.ingredient.price

        product_instance = {
            "id": i.product_instance.id,
            "name": i.product_instance.product.name,
            "total_price": i.product_instance.total_price,
            "product_name": i.product_instance.product.name,
            "ingredients": ingredients,
        }

        total += i.product_instance.total_price
        product_instances.append(product_instance)

    final_dict = {
        "id": cart.id,
        "product_instances": product_instances,
        "total": total,
        "quantity": len(product_instances),
        "created_at": cart.created_at,
        "updated_at": cart.updated_at
    }
    return final_dict
