from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from archives.models import User, Role, Category, AgeRating, Product, Image, Address, Favorite, UserProduct


class UserAdminConfig(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('-date_created',)

    add_fieldsets = (
        (None, {'fields': ('email','first_name', 'last_name', 'password', 'phone', 'image',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role',)}),
        ('Personal', {'fields': ('address',)}),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Address)
admin.site.register(Favorite)
admin.site.register(UserProduct)

admin.site.register(Product)
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(AgeRating)

admin.site.register(Image)


