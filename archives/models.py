from django.db.models import Model
from django.contrib import admin
# Create your models here.

from django.db import models

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

class User(BaseModel):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=XS)
    last_name = models.CharField(max_length=XS)
    email = models.CharField(max_length=S, unique=True)
    password = models.CharField(max_length=S)
    phone = models.CharField(max_length=S)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, default='A')
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email + ' ' + self.role.name

    class Meta:
        db_table = 'user'


class Role(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=XS)
    description = models.CharField(max_length=M)

    class Meta:
        db_table = 'role'


class Address(BaseModel):
    id = models.AutoField(primary_key=True)
    zip_code = models.CharField(max_length=XS)
    country = models.CharField(max_length=S)
    county = models.CharField(max_length=S)
    city = models.CharField(max_length=S)
    street = models.CharField(max_length=S)
    house_number = models.IntegerField(null=True, blank=True)
    apartment_number = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'address'


class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=M)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    year = models.IntegerField()
    stock = models.IntegerField()
    players_min = models.IntegerField()
    players_max = models.IntegerField()
    description = models.TextField(max_length=10000)
    status = models.CharField(max_length=1, default='A')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    age_rating = models.ForeignKey('AgeRating', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.category.name

    class Meta:
        db_table = 'product'


class AgeRating(BaseModel):
    id = models.AutoField(primary_key=True)
    minimum = models.IntegerField()
    description = models.CharField(max_length=M)

    class Meta:
        db_table = 'age_rating'


class Category(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=S)
    description = models.CharField(max_length=M)

    class Meta:
        db_table = 'category'


class Skill(BaseModel):
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=1)
    description = models.CharField(max_length=M)

    class Meta:
        db_table = 'skill'


class Image(BaseModel):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=M)

    class Meta:
        db_table = 'image'


# middle tables

class UserProduct(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1)

    class Meta:
        db_table = 'user_product'


class Favorite(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite'
