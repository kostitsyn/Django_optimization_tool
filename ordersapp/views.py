from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from mainapp.models import Games
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from django.db import models
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, request


class OrderListView(ListView):
    model = Order

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'заказы'
        return context_data


class OrderItemsCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(OrderItemsCreateView, self).get_context_data(**kwargs)
        context_data['title'] = 'создание заказа'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.get_items(self.request.user)

            if len(basket_item):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_item))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                    form.initial['quantity_storage'] = basket_item[num].product.quantity
            else:
                formset = OrderFormSet()

        context_data['orderitems'] = formset

        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            Basket.get_items(self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # if self.object.get_total_cost == 0:
        if self.object.get_summary['total_cost'] == 0:
            self.object.delete()

        return super(OrderItemsCreateView, self).form_valid(form)


class OrderItemsUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        context_data = super(OrderItemsUpdateView, self).get_context_data(**kwargs)
        context_data['title'] = 'редактирование заказа'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.initial['quantity_storage'] = form.instance.product.quantity
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']
        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            orderitems.save()

        # if self.object.get_total_cost == 0:
        if self.object.get_summary['total_cost'] == 0:
            self.object.delete()

        return super(OrderItemsUpdateView, self).form_valid(form)


class OrderItemsDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        context_data = super(OrderItemsDeleteView, self).get_context_data(**kwargs)
        context_data['title'] = 'удаление заказа'
        return context_data


class OrderItemsReadView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context_data = super(OrderItemsReadView, self).get_context_data(**kwargs)
        context_data['title'] = 'просмотр заказа'
        return context_data


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':

        if instance.pk:
            # instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
            instance.product.quantity = F('quantity') - (instance.quantity - sender.get_item(instance.pk).quantity)
        else:
            # instance.product.quantity -= instance.quantity
            instance.product.quantity = F('quantity') - instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    # instance.product.quantity += instance.quantity
    instance.product.quantity = F('quantity') + instance.quantity
    instance.product.save()


def get_product_price_quantity(request, pk):
    if request.is_ajax():
        product = Games.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price, 'quantity_storage': product.quantity})
        else:
            return JsonResponse({'price': 0, 'quantity_storage': 0})


