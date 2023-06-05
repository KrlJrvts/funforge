from django.views.generic import View

from archives.models import Category, User


# Create your views here.

# Products Views

class CategoriesView(View):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'


class CategoryCreateView(View):
    template_name = 'category_create.html'
    model = Category
    context_object_name = 'category'


class CategoryUpdateView(View):
    template_name = 'category_update.html'
    model = Category
    context_object_name = 'category'


# Users Views

class UsersView(View):
    template_name = 'users.html'
    model = User
    context_object_name = 'users'


class UserCreateView(View):
    template_name = 'user_create.html'
    model = User
    context_object_name = 'user'


class UserUpdateView(View):
    template_name = 'user_update.html'
    model = User
    context_object_name = 'user'
