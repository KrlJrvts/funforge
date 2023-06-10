from django.contrib import admin

from archives.models import User, Role, Category, AgeRating, Product, Image

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(AgeRating)
admin.site.register(Product)
admin.site.register(Image)
