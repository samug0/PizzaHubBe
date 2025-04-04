from django.contrib import admin
from pizza_hub_app.models import User, Role


# Registration of User Entity
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "last_name", "email", "username", "phone_number",
        "country", "address", "city", "profile_image", "email_verified_at",
        "phone_verified_at","refresh_token", "created_at", "updated_at"
    ]
    list_per_page = 20
    

    # Campi non editabili
    readonly_fields = ["id", "password", "refresh_token", "created_at", "updated_at", "phone_verified_at", "email_verified_at"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = [
       "id", "name", "created_at", "updated_at"
    ]
    list_per_page = 20

    # Campi non editabili
    readonly_fields = ["id", "created_at", "updated_at"]