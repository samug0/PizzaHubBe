from django.db import models
from uuid import uuid4
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.hashers import make_password
# Create your models here.


class RoleType(models.TextChoices):
    USER = "USER"
    ADMIN = "ADMIN"

class UserStatus(models.TextChoices):
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class OrderStatus(models.TextChoices):
    COMPLETED = "COMPLETED"
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class PaymentType(models.TextChoices):
    CASH  = "CASH"
    ONLINE = "ONLINE"


class PaymentStatus(models.TextChoices):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    FAILED = "FAILED"



class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(BaseModel):
    name = models.CharField(choices=RoleType, default=RoleType.USER, unique=True, max_length=30)

    class Meta:
        db_table = "Role"
        verbose_name_plural = "Ruoli"

    def __str__(self) -> str:
        return f'Ruole "{self.name}"'


class User(BaseModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=14, default=None, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    refresh_token = models.CharField(unique=True, null=True, default=None, max_length=300, blank=True)
    status = models.CharField(choices=UserStatus, default=UserStatus.CREATED, max_length=30, blank=True)
    password = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to="upload_user_image/", null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = "User"
        verbose_name_plural = "Utenti"

    def __str__(self) -> str:
        return f'Utente "{self.email}"'


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Carts"
        verbose_name_plural = "Carrelli"

    def __str__(self) -> str:
        return f'Carrello Utente "{self.user.email}"'



class Product(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    price = models.FloatField()
    ingredients = ArrayField(models.CharField(null=True, max_length=50), null=True)
    description = models.TextField(max_length=1000, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "Products"
        verbose_name_plural = "Prodotti"

    def __str__(self) -> str:
        return f'Prodotto "{self.name}"'



class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "CardProducts"
        verbose_name_plural = "CarrelloProdotto"
    
    def __str__(self) -> str:
        return f'Carrello Prodotto "{self.id}"'


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    approved = models.BooleanField(default=False)
    preparation_estimata = models.DateTimeField(null=True)
    status = models.CharField(choices=OrderStatus, default=OrderStatus.PENDING, max_length=30)
    is_payed = models.BooleanField(default=False)

    class Meta:
        db_table = "Orders"
        verbose_name_plural = "Ordini"

    def __str__(self) -> str:
        return f'Ordine utente "{self.user.email}"'

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    class Meta:
        db_table = "OrderProducts"
        verbose_name_plural = "Ordini Prodotto"

    def __str__(self) -> str:
        return f'Ordine Prodotto "{self.id}"'


class Payments(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(choices=PaymentStatus, default=PaymentStatus.PENDING, max_length=30)
    type = models.CharField(choices=PaymentType, default=PaymentType.ONLINE, max_length=30)

    class Meta:
        db_table = "Payments"
        verbose_name_plural = "Pagamenti"
    
    def __str__(self) -> str:
        return f'Pagamento Utente "{self.user.email}"'


class ProductPayment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE)

    class Meta:
        db_table = "ProductPaymets"
        verbose_name_plural = "Pagamento Prodotti"
    
    def __str__(self) -> str:
        return f'Carrello Prodotto "{self.id}"'


class AdditionalProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    price = models.FloatField()
    description = models.TextField(max_length=1000, null=True)

    class Meta:
        db_table = "AdditionalProduct"
        verbose_name_plural = "Prodotti Aggiungitvi"
    
    def __str__(self) -> str:
        return f'Prodotto aggiuntivo "{self.name}"'


class Category(BaseModel):
    name = models.CharField(unique=True, max_length=150)
    desription = models.TextField(max_length=1000, null=True)

    class Meta:
        db_table = "Category"
        verbose_name_plural = "Categorie"
    
    def __str__(self) -> str:
        return f'Categoria "{self.name}"'


class ProductCategory(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "ProductCategory"
        verbose_name_plural = "Categorie Prodotto"
    
    def __str__(self) -> str:
        return f'Categoria Prodotto "{self.id}"'


class CartProductExtra(BaseModel):
    additional_product = models.ForeignKey(AdditionalProduct, on_delete=models.CASCADE)
    cart_product = models.ForeignKey(CartProduct, on_delete=models.CASCADE)

    class Meta:
        db_table = "CartProductExtra"
        verbose_name_plural = "Prodotto carrello extra"
    
    def __str__(self) -> str:
        return f'Prodotto carrello extra "{self.id}"'


