from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from utils import forms


from archives.models import Category, Product, Favorite
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


from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Get the category of the current product
    category = product.category_id

    # Get other games in the same category
    other_games = Product.objects.filter(category_id=category).exclude(pk=pk)

    context = {
        'product': product,
        'other_games': other_games,
        'category': category,
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
            return redirect(reverse('store/store.html'))
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


def favorite_view(request):
    all_favorites = Favorite.objects.all()
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


