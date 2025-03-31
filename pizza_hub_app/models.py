from django.db import models
from uuid import uuid4
# Create your models here.


class BaseModel(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=14, default=None)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    profile_image = models.ImageField(upload_to="upload_user_image/", null=True, blank=True)


    class Meta:
        db_table = "User"
        verbose_name_plural = "User"

    def __str__(self) -> str:
        return f'User "{self.email}"'