from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView

import basketapp
from basketapp.models import Basket
from mainapp.models import Games


class BasketListView(ListView):
    model = Basket
    template_name = 'basketapp/basket.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        basket_items = Basket.objects.filter(user=self.request.user)
        return basket_items

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'корзина'
        return context_data


# @login_required
# def basket(request):
#
#     title = 'корзина'
#
#     basket_items = Basket.objects.filter(user=request.user)
#
#     print('hello')
#     print(basket_items)
#
#     content = {
#         'title': title,
#         'basket_items': basket_items,
#     }
#
#     return render(request, 'basketapp/basket.html', content)


# class BasketUpdateView(UpdateView):
#     model = Basket
#     template_name = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     success_url = reverse_lazy(request.META.get('HTTP_REFERER'))
#     fields = '__all__'


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        game_name = Games.objects.get(pk=pk).name
        return HttpResponseRedirect(reverse('gallery:game', args=[game_name]))
    product_item = get_object_or_404(Games, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket.objects.create(product=product_item, user=request.user)

    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# class BasketRemoveDeleteView(DeleteView):
#     model = Basket
#     template_name = 'basketapp/basket.html'
#     success_url = reverse_lazy('basket:basket')

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     print('world')
    #     print(args)
    #     print(kwargs)
    #     return super().dispatch(*args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object(**kwargs)
    #     print('hello')
    #     print(self.object)
    #     self.object.delete()
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # def get_success_url(self):
    #     product_pk = self.kwargs.get('pk', None)
    #     print('hello')
    #     print(product_pk)
    #     return reverse_lazy('admin:products', args=[product_pk])



@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user)
        content = {
            'basket_items': basket_items
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})