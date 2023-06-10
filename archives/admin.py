from django.contrib import admin

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass


class Author:
    pass


admin.site.register(Author, AuthorAdmin)
