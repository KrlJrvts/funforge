from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from archives.models import Category, Product


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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('status')
        user = authenticate(request, email=username, password=password, status=status)
        if user is not None and status == 'A':
            login_view(request, user)
            return redirect(reverse('store:store'))
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
