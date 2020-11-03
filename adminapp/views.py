from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, GameEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.models import GameCategories, Games
from ordersapp.models import Order


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users', args=[1])
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'пользователи/создание'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users', args=[1]))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {
#         'name_page': title,
#         'update_form': user_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', content)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 2

    @method_decorator(user_passes_test((lambda u: u.is_superuser)))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'админка/пользователи'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     content = {
#         'title': title,
#         'objects': users_list,
#     }
#     return render(request, 'adminapp/users.html', content)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users', args=[1])
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'пользователи/редактирование'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#     else:
#         user_form = ShopUserAdminEditForm(instance=edit_user)
#     content = {
#         'name_page': title,
#         'update_form': user_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', content)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users', args=[1])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.method == 'POST' and self.object.is_active:
            self.object.is_active = False
            self.object.save()
        else:
            if self.object.is_active == False:
                self.object.is_active = True
                self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'пользователи/удаление'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#
#     title = 'пользователи/удаление'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST' and edit_user.is_active:
#         edit_user.is_active = False
#         edit_user.save()
#         return HttpResponseRedirect(reverse('admin:users', args=[1]))
#     else:
#         if edit_user.is_active == False:
#             edit_user.is_active = True
#             edit_user.save()
#             return HttpResponseRedirect(reverse('admin:users', args=[1]))
#
#     content = {'name_page': title,
#                'user_to_delete': edit_user
#                }
#     return render(request, 'adminapp/user_delete.html', content)


class ProductCategoryCreateView(CreateView):
    model = GameCategories
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories', args=[1])
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'категории/создание'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#     content = {
#         'name_page': title,
#         'update_form': category_form,
#     }
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoriesListView(ListView):
    model = GameCategories
    template_name = 'adminapp/categories.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'админка/категории'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request, page=1):
#
#     title = 'админка/категории'
#
#     categories_list = GameCategories.objects.all()
#
#     paginator = Paginator(categories_list, 3)
#     try:
#         categories_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         categories_paginator = paginator.page(1)
#     except EmptyPage:
#         categories_paginator = paginator.page(paginator.num_pages)
#
#     content = {
#         'name_page': title,
#         'objects': categories_paginator,
#     }
#     return render(request, 'adminapp/categories.html', content)


class ProductCategoryUpdateView(UpdateView):
    model = GameCategories
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories', args=[1])
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'категории/редактирование'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#
#     title = 'категории/редактирование'
#
#     category_item = get_object_or_404(GameCategories, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=category_item)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[category_item.pk]))
#     else:
#         category_form = ProductCategoryEditForm(instance=category_item)
#     content = {
#         'name_page': title,
#         'update_form': category_form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryDeleteView(DeleteView):
    model = GameCategories
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories', args=[1])
    paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        products_of_category = Games.objects.filter(game_category=self.object.pk)

        if request.method == 'POST' and self.object.is_active:
            self.object.is_active = False
            self.object.save()
            for item in products_of_category:
                item.is_active = False
                item.save()
        else:
            if self.object.is_active == False:
                self.object.is_active = True
                self.object.save()
                for item in products_of_category:
                    item.is_active = True
                    item.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'категории/удаление'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#
#     title = 'категории/удаление'
#
#     category_item = get_object_or_404(GameCategories, pk=pk)
#     products_of_category = Games.objects.filter(game_category=category_item.pk)
#
#     if request.method == 'POST' and category_item.is_active:
#         category_item.is_active = False
#         category_item.save()
#         for item in products_of_category:
#             item.is_active = False
#             item.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         if category_item.is_active == False:
#             category_item.is_active = True
#             category_item.save()
#             for item in products_of_category:
#                 item.is_active = True
#                 item.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title,
#                'category_to_delete': category_item
#                }
#     return render(request, 'adminapp/category_delete.html', content)


class ProductCreateView(CreateView):
    model = Games
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products', args=[1, 1])
    form_class = GameEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_pk = self.kwargs.get('pk', None)
        context_data['title'] = 'продукты/создание'
        context_data['game_category'] = get_object_or_404(GameCategories, pk=category_pk)
        context_data['form']['game_category'].initial = get_object_or_404(GameCategories, pk=category_pk)
        return context_data

    def get_success_url(self):
        category_pk = self.object.game_category.pk
        return reverse_lazy('admin:products', args=[category_pk, 1])


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#
#     title = 'продукты/создание'
#
#     category_item = GameCategories.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         product_form = GameEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[category_item.pk]))
#     else:
#         product_form = GameEditForm(initial={'game_category': category_item})
#     content = {
#         'name_page': title,
#         'update_form': product_form,
#         'category': category_item,
#     }
#     return render(request, 'adminapp/product_update.html', content)


class ProductsListView(ListView):
    model = Games
    template_name = 'adminapp/products.html'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u : u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_pk = self.kwargs.get('pk', None)
        context_data['title'] = 'категории/игры'
        context_data['game_category'] = get_object_or_404(GameCategories, pk=category_pk)
        return context_data

    def get_queryset(self):
        category_pk = self.kwargs.get('pk', None)
        games_by_category = Games.objects.filter(game_category=category_pk)
        return games_by_category


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk, page=1):
#
#     title = 'категории/игры'
#
#     category_item = get_object_or_404(GameCategories, pk=pk)
#     products_list = Games.objects.filter(game_category=category_item)
#
#     paginator = Paginator(products_list, 3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     content = {
#         'title': title,
#         'objects': products_paginator,
#         'category': category_item,
#     }
#
#     return render(request, 'adminapp/products.html', content)


class ProductDetailView(DetailView):
    model = Games
    template_name = 'adminapp/product.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'админка/игра'
        context_data['css_file'] = 'style-admin.css'
        context_data['game_category'] = GameCategories.objects.get(name=self.object.game_category)
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#
#     title = 'админка/игра'
#
#     product_item = get_object_or_404(Games, pk=pk)
#     category_item = GameCategories.objects.get(name=product_item.game_category)
#
#
#     content = {
#         'title': title,
#         'objects': product_item,
#         'category': category_item,
#     }
#
#     return render(request, 'adminapp/product.html', content)


# class ProductUpdateView(UpdateView):
#     model = Games
#     template_name = 'adminapp/product_update.html'
#     success_url = reverse_lazy('admin:products', args)


class ProductUpdateView(UpdateView):
    model = Games
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:products', args=[1, 1])
    form_class = GameEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_pk = self.kwargs.get('pk', None)
        context_data['title'] = 'игры/редактирование'
        category_pk = Games.objects.get(pk=product_pk).game_category.pk
        context_data['game_category'] = get_object_or_404(GameCategories, pk=category_pk)
        return context_data

    def get_success_url(self):
        category_pk = self.object.game_category.pk
        return reverse_lazy('admin:products', args=[category_pk, 1])


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#
#     title = 'игры/редактирование'
#
#     product_item = get_object_or_404(Games, pk=pk)
#     category_item = GameCategories.objects.get(name=product_item.game_category)
#
#     if request.method == 'POST':
#         product_form = GameEditForm(request.POST, request.FILES, instance=product_item)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:product_update', args=[product_item.pk]))
#     else:
#         product_form = GameEditForm(instance=product_item)
#     content = {
#         'name_page': title,
#         'update_form': product_form,
#         'category': category_item,
#     }
#     return render(request, 'adminapp/product_update.html', content)


class ProductDeleteView(DeleteView):
    model = Games
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin:products', args=[1, 1])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.method == 'POST' and self.object.is_active:
            self.object.is_active = False
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            if self.object.is_active == False:
                self.object.is_active = True
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        product_pk = self.kwargs.get('pk', None)
        category_pk = Games.objects.get(pk=product_pk).game_category.pk
        return reverse_lazy('admin:products', args=[category_pk, 1])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'игры/удаление'
        return context_data


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#
#     title = 'игры/удаление'
#
#     product_item = get_object_or_404(Games, pk=pk)
#     category_item = GameCategories.objects.get(name=product_item.game_category)
#
#     if request.method == 'POST' and product_item.is_active:
#         product_item.is_active = False
#         product_item.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[category_item.pk]))
#     else:
#         if product_item.is_active == False:
#             product_item.is_active = True
#             product_item.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[category_item.pk]))
#
#     content = {'title': title,
#                'product_to_delete': product_item,
#                'category': category_item,
#                }
#     return render(request, 'adminapp/product_delete.html', content)


class OrdersListView(ListView):
    model = Order
    template_name = 'adminapp/orders.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        statuses_tuple = Order.ORDER_STATUSES
        all_statuses = []
        for status in statuses_tuple:
            all_statuses.append(status[1])

        context_data['statuses'] = all_statuses

        context_data['title'] = 'админка/заказы'
        return context_data


class OrderEditStatusView(UpdateView):
    model = Order
    template_name = 'adminapp/orders.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        new_item_pk = self.kwargs.get('pk', None)
        new_status = self.kwargs.get('status', None)
        object = Order.objects.get(pk=new_item_pk)
        object.status = new_status
        object.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @user_passes_test(lambda u: u.is_superuser)
# def order_edit(request, pk, status):
#     if request.is_ajax():
#
#         new_order_item = Order.objects.get(pk=pk)
#         orders = Order.objects.all()
#         new_order_item.status = status
#         new_order_item.save()
#         content = {
#             'object_list': orders
#         }
#
#         result = render_to_string('adminapp/orders.html', content)
#
#         return JsonResponse({'result': result})
#     else:
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


