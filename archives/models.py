from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.db import models
from django.db.models import Model

# MAX LENGTHS
XS = 10
S = 50
M = 255
L = 1000
XL = 1000


# NonNullableNonBlankModel
class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self._meta.fields:
            if not field.null:
                field.null = False
            if not field.blank:
                field.blank = False


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            first_name=self.capitalize(first_name),
            last_name=self.capitalize(last_name),
            email=self.normalize_email(email),
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=self.capitalize(first_name),
            last_name=self.capitalize(last_name),
            email=self.normalize_email(email),
            password=password,
        )

        user.role_id = 1
        user.save(using=self._db)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=XS)
    last_name = models.CharField(max_length=XS)
    email = models.EmailField(verbose_name="email", max_length=S, unique=True)
    password = models.CharField(max_length=S)
    phone = models.CharField(max_length=S)
    date_created = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=1, default='A')
    address = models.ForeignKey('Address', on_delete=models.DO_NOTHING)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, default=3)
    image = models.ForeignKey('Image', on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.role.name} {self.email}"

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'user'

    groups = models.ManyToManyField(Group, related_name='users_archive')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='users_archive',
        blank=True,
    )


class Role(BaseModel):
    name = models.CharField(max_length=XS)
    description = models.CharField(max_length=M)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'


class Address(BaseModel):
    zip_code = models.CharField(max_length=XS)
    country = models.CharField(max_length=S)
    county = models.CharField(max_length=S)
    city = models.CharField(max_length=S)
    street = models.CharField(max_length=S)
    house_number = models.IntegerField(null=True, blank=True)
    apartment_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.country + ', ' + self.city + ', ' + self.street + ' ' + self.zip_code

    class Meta:
        db_table = 'address'


class Product(BaseModel):
    name = models.CharField(max_length=M)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    year = models.IntegerField()
    stock = models.IntegerField()
    players_min = models.IntegerField()
    players_max = models.IntegerField()
    description = models.TextField(max_length=10000)
    status = models.CharField(max_length=1, default='A')
    category_id = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    image = models.ForeignKey('Image', on_delete=models.DO_NOTHING, null=True, blank=True)
    skill = models.ForeignKey('Skill', on_delete=models.DO_NOTHING)
    age_rating = models.ForeignKey('AgeRating', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name + ' - ' + self.category_id.name + ' - ' + str(self.stock)

    class Meta:
        db_table = 'product'


class AgeRating(BaseModel):
    minimum = models.IntegerField()
    description = models.CharField(max_length=M)

    def __str__(self):
        return f'{self.minimum} ({self.description})'

    class Meta:
        db_table = 'age_rating'


class Category(BaseModel):
    name = models.CharField(max_length=S)
    description = models.CharField(max_length=M)

    def __str__(self):
        return self.name + ' - ' + self.description

    class Meta:
        db_table = 'category'


class Skill(BaseModel):
    level = models.CharField(max_length=1)
    description = models.CharField(max_length=M)

    def __str__(self):
        return f'{self.level} - ({self.description})'

    class Meta:
        db_table = 'skill'


class Image(BaseModel):
    name = models.CharField(max_length=S, null=True, blank=True)
    image = models.ImageField(upload_to='static/images/products', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'image'


# joint tables

class UserProduct(BaseModel):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1)

    class Meta:
        db_table = 'user_product'


class Favorite(BaseModel):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite'
