from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'заказы'
        return context_data


class OrderItemsCreateView(CreateView):
    model = Order
    fields = []
    sucess_url = reverse_lazy('')

    def get_context_data(self, **kwargs):
        context_data = super(OrderItemsCreateView, self).get_context_data(**kwargs)
        context_data['title'] = 'создание заказа'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            formset = OrderFormSet()

        context_data['orderitems'] = formset

        return context_data
