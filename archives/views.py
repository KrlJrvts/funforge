from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from archives.models import Category


# Create your views here.

class CategoriesView(View):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'

