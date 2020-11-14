"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    # path('<page>/', mainapp.gallery, name='gallery_main'),
    path('<page>/', mainapp.GalleryListView.as_view(), name='gallery_main'),

    # path('category/<int:pk>/<page>/', mainapp.by_category, name='category'),
    path('category/<int:pk>/<page>/', mainapp.ByCategoryListView.as_view(), name='category'),

    # path('product/<str:pk>', mainapp.product, name='game'),
    path('product/<pk>/', mainapp.ProductDetailView.as_view(), name='game'),
    # path('product/<pk>/', cache_page(3600, key_prefix='geekshop')(mainapp.ProductDetailView.as_view()), name='game'),

    path('category/<int:pk>/<page>/ajax/', cache_page(3600)(mainapp.product_ajax)),
]
