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
import ordersapp.views as ordersapp


app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='orders_list'),
    path('create/', ordersapp.OrderItemsCreateView.as_view(), name='order_create'),
    path('read/<pk>/', ordersapp.OrderItemsReadView.as_view(), name='order_read'),
    path('update/<pk>/', ordersapp.OrderItemsUpdateView.as_view(), name='order_update'),
    path('delete/<pk>/', ordersapp.OrderItemsDeleteView.as_view(), name='order_delete'),
    path('forming/<pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),

    path('product/<pk>/price/', ordersapp.get_product_price_quantity),
]
