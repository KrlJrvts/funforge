from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from archives.models import Category, Product, Favorite, User
from utils import forms
from utils.forms import EditProfileForm


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


def product_detail_view(request, pk):
    product_details = Product.objects.get(pk=pk)
    context = {
        'product': product_details,
    }
    return render(request, './store/product-detail.html', context)


# user views


# login view should be in menu and it should take in user email and password, check if user exists and if email and
# password is correct. if they are correct, redirect to index page, if not, display error message in login modal.
# at the moment i can't get error and will not redirect to index page
# Error 405:
# Method Not Allowed (POST): /
# Method Not Allowed: /
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

# def login_view(request):
#     if request.method == 'GET':
#         return render(request, 'user/login.html')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user and user.status == 'A':
#             login(request, user)
#             return redirect(reverse('index'))
#         else:
#             messages.error(request, 'Invalid credentials')
#     # return render(request, 'user/login.html')
#     return render(request, 'index.html')




def login_view(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.status == 'A':
            login(request, user)
            return redirect('index')  # Redirect to the 'index' URL name
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'user/login.html')


# def index_view(request):
#     if request.method == 'GET':
#         return render(request, 'user/login.html')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#         else:
#             messages.error(request, 'Invalid credentials')
#     # return render(request, 'user/login.html')
#     return render(request, './index.html')


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


def user_profile_edit_view(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('index')
    else:
        form = EditProfileForm(instance=user)

    return render(request, './user/edit_profile.html', {'form': form})


def favorite_add_view(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)

        favourite, created = Favorite.objects.get_or_create(user=request.user)

        if product in favourite.products.all():
            messages.warning(request, "Product is already in Funforge favorites.")
        else:
            favourite.products.add(product)
            messages.success(request, "Product successfully added to favorites.")

    return redirect('favorite')


def favorite_remove_view(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)

        favorite = Favorite.objects.get(user=request.user)

        if product in favorite.products.all():
            favorite.products.remove(product)
            messages.success(request, "Product successfully removed from favorites.")
        else:
            messages.warning(request, "Product is not in favorites.")

    return redirect('favorite')


@login_required
def favorite_view(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    # filter favorites by user
    all_favorites = Favorite.objects.filter(user=user)
    context = {
        'all_favorites': all_favorites,
    }
    return render(request, './user/favorite.html', context)


# filter favorites by user


def cart_view(request):
    pass


# update stock (remove bought qty from stock) and add to cart


def cart_add_view(request):
    pass


# add product to cart


def cart_remove_view(request):
    pass

# remove product from cart
