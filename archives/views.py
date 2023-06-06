from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render
from utils.forms import AddGameForm

from archives.models import (
    Address,
    AgeRating,
    Category,
    Favorite,
    Image,
    Product,
    Role,
    Skill,
    User,
    UserProduct
)


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


# Admin Views


def add_game(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data and save the game
            # Access form field values using form.cleaned_data['field_name']
            # For example: game_name = form.cleaned_data['game_name']
            # Save the game to the database or perform other operations
            return render(request, 'success.html')  # Render a success page
    else:
        form = AddGameForm()

    return render(request, 'admin/add_game.html', {'form': form})


