from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    # path('', basketapp.basket, name='basket'),
    path('', basketapp.BasketListView.as_view(), name='basket'),

    path('add/<pk>/', basketapp.basket_add, name='add'),
    path('add/<pk>/', basketapp.basket_add, name='add'),

    # path('remove/<pk>/', basketapp.basket_remove, name='remove'),
    path('remove/<pk>/', basketapp.BasketDeleteView.as_view(), name='remove'),

    path('edit/<int:pk>/<quantity>/', basketapp.edit, name='edit'),
    # path('edit/<int:pk>/<quantity>/', basketapp.BasketUpdateView.as_view(), name='edit'),
]
