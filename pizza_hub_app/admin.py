from django.contrib import admin
from pizza_hub_app.models import Product, User, Role, BlackListToken, ProductImages, Ingredients, ProductIngredients, Category, ProductCategory


#Registration of User Entity
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "name", "last_name", "email", "username", "phone_number",
        "country", "address", "city", "status", "profile_image", "email_verified_at",
        "phone_verified_at"
    ]
    list_per_page = 20

    # Campi non editabili
    readonly_fields = ["id", "password", "refresh_token", "created_at", "updated_at", "phone_verified_at", "email_verified_at"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
       "name"
    ]
    list_per_page = 20

    # Campi non editabili
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(BlackListToken)
class BlackListTokenAdmin(admin.ModelAdmin):
    list_display = [
       "user","token", "expires_at", "is_valid"
    ]
    list_per_page = 20

    # Campi non editabili
    readonly_fields = [ "id", "user","token", "expires_at", "is_valid", "created_at", "updated_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "is_available"]
    list_per_page = 20
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "is_available"]
    list_per_page = 20
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(ProductIngredients)
class ProductIngredientsAdmin(admin.ModelAdmin):
    list_display = ["product", "ingredient"]
    list_per_page = 20
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(ProductImages)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "image"]
    list_per_page = 20
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    list_per_page = 20
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["product", "category"]
    list_per_page = 20
    readonly_fields = ["id", "created_at", "updated_at"]