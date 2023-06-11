from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from archives.models import Category, Product


def category(request):
    all_category = Category.objects.all()
    context = {
        'all_categories': all_category,
    }
    return render(request, './store/category.html', context)


def view_product(request):
    all_product = Product.objects.all()
    context = {
        'all_product': all_product,
    }
    return render(request, './store/store.html', context)


def product_detail(request, pk):
    product_details = Product.objects.get(pk=pk)
    context = {
        'product': product_details,
    }
    return render(request, './store/product-detail.html', context)


# def cart(request):
#     return render(request, 'cart.html')
#
#
# def calculate_total_price(cart_items):
#     total_price = 0
#     for item in cart_items:
#         total_price += item.price * item.quantity
#     return total_price
#
#
# def checkout(request):
#     return render(request, 'checkout.html')