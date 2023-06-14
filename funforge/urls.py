"""
URL configuration for funforge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from archives.views import products_view, categories_view, product_detail_view, login_view, logout_view, register_view, \
    favorite_add_view, favorite_remove_view, favorite_view

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # store
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('category/', categories_view, name='category'),
    path('store/', products_view, name='store'),
    path('store/<int:pk>/', product_detail_view, name='product_detail'),

    # user
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('favorite_view/', favorite_view, name='favorite'),
    path('add_favorite/', favorite_add_view, name='add-favorite'),
    path('remove_favorite/', favorite_remove_view, name='remove-favorite'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

