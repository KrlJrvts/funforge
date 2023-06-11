from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from archives.models import Category, Product
from utils import forms


def categories_view(request):
    all_category = Category.objects.all()
    context = {
        'all_categories': all_category,
    }
    return render(request, './store/category.html', context)


def products_view(request):
    all_product = Product.objects.filter(status='A')
    context = {
        'all_product': all_product,
    }
    return render(request, './store/store.html', context)


def products_all_view(request):  # for admin and staff
    pass


def product_detail_view(request, pk):
    product_details = Product.objects.get(pk=pk)
    context = {
        'product': product_details,
    }
    return render(request, './store/product-detail.html', context)


# user views

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('status')
        user = authenticate(request, email=username, password=password, status=status)
        if user is not None and status == 'A':
            login(request, user)
            return redirect(reverse('store'))
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def register_view(request):
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = forms.RegisterUserForm()
    return render(request, './user/register.html', {'form': form})


def user_edit_view(request):
    pass


# edit name, address, phone number, email, password, image
#     if request.method = 'PATCH':
#         pass


def favorite_add_view(request):
    pass


# add fav product to user

def favorite_remove_view(request):
    pass


# remove fav product from user,


def favorite_view(request):
    pass


# see fav product of user


def cart_view(request):
    pass


# update stock (remove bought qty from stock) and add to cart


def cart_add_view(request):
    pass


# add product to cart


def cart_remove_view(request):
    pass

# remove product from cart
