from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from archives.models import Category, Product, Favorite, User, UserProduct, Address
from utils.forms import EditProfileForm, RegisterUserForm


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
class UserLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    template_name = 'user/logout.html'







# def login_view(request):
#     if request.method == 'GET':
#         return render(request, 'user/login.html')
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('store')  # Redirect to the 'index' URL name
#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, redirect('index'))


@login_required
def logout_view(request):
    logout(request)
    return reverse('index')


def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone_number']
            zip_code = form.cleaned_data['zip_code']
            country = form.cleaned_data['country']
            county = form.cleaned_data['county']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            house_number = form.cleaned_data['house_number']
            apartment_number = form.cleaned_data['apartment_number']

            # Create an Address object
            address = Address.objects.create(
                zip_code=zip_code,
                country=country,
                county=county,
                city=city,
                street=street,
                house_number=house_number,
                apartment_number=apartment_number
            )

            # Create the User object and associate the Address
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address  # Associate the Address object
            )

            return redirect('login')

            # Additional processing or redirect to success page

    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'user/register.html', context)


@login_required
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


@login_required
def favorite_add_view(request, product_id):
    user = request.user

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        favourite, created = Favorite.objects.get_or_create(user=user)

        if product in favourite.products.all():
            messages.warning(request, "Product is already in your favorites.")
        else:
            favourite.products.add(product)
            messages.success(request, "Product successfully added to favorites.")

    return redirect('favorite')


@login_required
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


@login_required
def cart_view(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    all_cart = UserProduct.objects.filter(user=user)
    context = {
        'all_cart': all_cart,
    }
    return render(request, './user/cart.html', context)


# update stock (remove bought qty from stock) and add to cart

@login_required
def cart_add_view(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        qty = request.POST.get('qty')
        if product.stock >= int(qty):
            product.stock -= int(qty)
            product.save()
            user_product = UserProduct.objects.create(user=user, product=product, qty=qty)
            user_product.save()
            messages.success(request, "Product successfully added to cart.")
        else:
            messages.warning(request, "Not enough stock.")


# add product to cart

@login_required
def cart_remove_view(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user_product = get_object_or_404(UserProduct, user=user, product_id=product_id, status='A')

        # Decrease the stock of the product
        product = user_product.product
        product.stock += user_product.qty
        product.save()

        # Remove the item from the user's cart
        user_product.delete()

        messages.success(request, "Product successfully removed from cart.")

    return redirect('cart_view')

# remove product from cart
