import random

from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.base import View, ContextMixin, TemplateView
from django.template.loader import render_to_string
from basketapp.models import Basket
from geekshop import settings
from mainapp.models import Games, Contacts, DiscountGames, GameCategories


def get_hot_product():
    games_list = Games.objects.all().exclude(quantity=0)
    if games_list:
        return random.sample(list(games_list), 1)[0]
    else:
        return None


def get_required_obj(lst, num, max_num=0):
    my_list = []
    i = 1
    while i <= num:
        rand_num = random.randint(0, len(lst) - 1)
        my_list.append(lst.pop(rand_num))
        i += 1
        if i == max_num + 1 and max_num != 0:
            break
    return my_list


class MainListView(ListView):
    model = Games
    template_name = 'mainapp/index.html'

    # @method_decorator(cache_page(3600))
    # def dispatch(self, *args, **kwargs):
    #     return super(MainListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        result_list = list(Games.objects.all().select_related())[:4]
        # game_list = list(Games.objects.all().select_related())
        # result_list = get_required_obj(game_list, 4)

        return result_list

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'главная'
        context_data['css_file'] = 'style-index.css'
        context_data['contact_data'] = Contacts.objects.all()[0]

        return context_data


class AboutTemplateView(TemplateView):
    template_name = 'mainapp/about.html'

    @method_decorator(cache_page(3600))
    def dispatch(self, *args, **kwargs):
        return super(AboutTemplateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'о нас'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


class ServiceTemplateView(TemplateView):
    template_name = 'mainapp/services.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'услуги'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


class GalleryListView(ListView):
    model = Games
    template_name = 'adminapp/games_list.html'
    paginate_by = 4

    def get_queryset(self):
        global hot_product
        hot_product = get_hot_product()
        if hot_product:
            rest_games = Games.objects.all().exclude(pk=hot_product.pk)
            return rest_games
        else:
            return Games.objects.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'галлерея'
        context_data['css_file'] = 'style-gallery.css'
        if hot_product:
            context_data['hot_product'] = hot_product
        context_data['links_menu'] = GameCategories.objects.all()
        # context_data['links_menu'] = get_links_menu()
        context_data['games_discount'] = DiscountGames.objects.all()
        return context_data


class ByCategoryListView(ListView):
    model = Games
    template_name = 'mainapp/games_by_category.html'
    paginate_by = 4

    def get_queryset(self):
        category_pk = self.kwargs.get('pk', None)
        if category_pk:
            games_by_category = Games.objects.filter(game_category=category_pk)
        else:
            games_by_category = Games.objects.all()
        return games_by_category

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'категории'
        context_data['css_file'] = 'style-gallery.css'
        category_pk = self.kwargs.get('pk', None)
        if category_pk == 0:
            context_data['category'] = {'name': 'все', 'pk': category_pk}
        else:
            context_data['category'] = get_object_or_404(GameCategories, pk=category_pk)
        context_data['links_menu'] = GameCategories.objects.all()
        # context_data['links_menu'] = get_links_menu()
        hot_product = get_hot_product()
        if hot_product:
            context_data['hot_product'] = hot_product
        context_data['games_discount'] = DiscountGames.objects.all()
        return context_data


class NewsTemplateView(TemplateView):

    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'новости'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


class TeamTemplateView(TemplateView):
    template_name = 'mainapp/team.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'сотрудники'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


class ContactsListView(ListView):
    model = Contacts
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contact_data'] = Contacts.objects.all()[0]
        context_data['title'] = 'контакты'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


class ProductDetailView(DetailView):
    model = Games

    # def get_object(self, queryset=None):
    #     self.object = super().get_object()
    #     item_pk = self.object.pk
    #     self.object = get_product(item_pk)
    #     return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        game_pk = self.kwargs.get('pk', None)
        category = Games.objects.get(pk=game_pk).game_category.pk
        context_data['object_list'] = Games.objects.filter(game_category=category).exclude(pk=game_pk).order_by('?')[:4]
        context_data['title'] = 'товары'
        context_data['css_file'] = 'style-product-page.css'
        context_data['contact_data'] = Contacts.objects.get(pk=1)
        return context_data


# def get_links_menu():
#     if settings.LOW_CACHE:
#         key = 'links_menu'
#         links_menu = cache.get(key)
#         if links_menu is None:
#             links_menu = GameCategories.objects.filter(is_active=True)
#             cache.set(key, links_menu)
#         return links_menu
#     else:
#         return GameCategories.objects.filter(is_active=True)
#
# def get_category(pk):
#     if settings.LOW_CACHE:
#         key = f'category_{pk}'
#         category = cache.get(key)
#         if category is None:
#             category = get_object_or_404(GameCategories, pk=pk)
#             cache.set(key, category)
#         return category
#     else:
#         return get_object_or_404(GameCategories, pk=pk)
#
# def get_products():
#     if settings.LOW_CACHE:
#         key = 'products'
#         products = cache.get(key)
#         if products is None:
#             products = Games.objects.all()
#             cache.set(key, products)
#         return products
#     else:
#         return Games.objects.all()
#
# def get_products_by_category(pk):
#     if settings.LOW_CACHE:
#         key = f'products_by_category_{pk}'
#         products_by_category = cache.get(key)
#         if products_by_category is None:
#             products_by_category = Games.objects.filter(game_category=pk)
#             cache.set(key, products_by_category)
#         return products_by_category
#     else:
#         return Games.objects.filter(game_category=pk)
#
# def get_product(pk):
#     if settings.LOW_CACHE:
#         key = f'product_{pk}'
#         product = cache.get(key)
#         if product is None:
#             product = Games.objects.get(pk=pk)
#             cache.set(key, product)
#         return product
#     else:
#         return Games.objects.get(pk=pk)
#
# def get_hot_product():
#     if settings.LOW_CACHE:
#         key = 'hot_product'
#         hot_product = cache.get(key)
#         if hot_product is None:
#             games_list = Games.objects.all().exclude(quantity=0)
#             hot_product = random.sample(list(games_list), 1)[0]
#             cache.set(key, hot_product)
#         return hot_product
#     else:
#         games_list = Games.objects.all().exclude(quantity=0)
#         hot_product = random.sample(list(games_list), 1)[0]
#         return hot_product

# @cache_page(3600)
# def main(request, pk=None):
#
#     title = 'главная'
#
#     contact_data = Contacts.objects.get(pk=1)
#     game_list = list(Games.objects.all())
#     # result_list = get_required_obj(game_list, 4)
#     result_list = list(Games.objects.all().select_related())[:3]
#     content = {
#         'title': title,
#         'css_file': 'style-index.css',
#         'object_list': result_list,
#         'contact_data': contact_data,
#     }
#     return render(request, 'mainapp/index.html', content)

# def about(request):
#
#     title = 'о нас'
#
#     content = {
#         'title': title,
#         'css_file': 'style-gallery.css',
#     }
#
#     return render(request, 'mainapp/about.html', content)

# def service(request):
#
#     title = 'услуги'
#
#     content = {
#         'title': title,
#         'css_file': 'style-gallery.css',
#     }
#
#     return render(request, 'mainapp/services.html', content)

# def gallery(request, page=1):
#
#     title = 'галлерея'
#
#     # links_menu = GameCategories.objects.all()
#     links_menu = get_links_menu()
#
#     hot_product = get_hot_product()
#     games_list = list(Games.objects.all().exclude(pk=hot_product.pk))
#
#     game_discount = list(DiscountGames.objects.all())
#     result_list_discount = get_required_obj(game_discount, 2)
#
#     paginator = Paginator(games_list, 4)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     content = {
#         'title': title,
#         'css_file': 'style-gallery.css',
#         'links_menu': links_menu,
#         'object_list': products_paginator,
#         'games_discount': result_list_discount,
#         'hot_product': get_hot_product()
#     }
#     return render(request, 'mainapp/games_list.html', content)

# def product_ajax(request, pk=None, page=1):
#     if request.is_ajax():
#         links_menu = get_links_menu()
#
#         if pk == 0:
#             category = {'name': 'все', 'pk': pk}
#             products = get_products()
#         else:
#             category = get_category(pk)
#             products = get_products_by_category(pk)
#         paginator = Paginator(products, 4)
#         try:
#             products_paginator = paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator = paginator.page(1)
#         except EmptyPage:
#             products_paginator = paginator.page(paginator.num_pages)
#
#         content = {
#             'links_menu': links_menu,
#             'category': category,
#             'products': products_paginator,
#         }
#
#         result = render_to_string(
#             'mainapp/includes/inc_products_list_content.html',
#             content,
#             request
#         )
#
#         return JsonResponse({'result': result})

# def by_category(request, pk, page=1):
#
#     title = 'категории'
#
#     # links_menu = GameCategories.objects.all()
#     links_menu = get_links_menu()
#     if pk == 0:
#         games_list = Games.objects.all()
#         category = {'name': 'все', 'pk': pk}
#     else:
#         # category = get_object_or_404(GameCategories, pk=pk)
#         category = get_category(pk)
#         games_list = Games.objects.filter(game_category=category).order_by('name')
#
#     paginator = Paginator(games_list, 4)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     game_discount = list(DiscountGames.objects.all())
#     result_list_discount = get_required_obj(game_discount, 2)
#     content = {'title': title,
#                'css_file': 'style-gallery.css',
#                'links_menu': links_menu,
#                'object_list': products_paginator,
#                'hot_product': get_hot_product(),
#                'games_discount': result_list_discount,
#                'category': category,
#                }
#
#     return render(request, 'mainapp/games_by_category.html', content)

# def news(request):
#
#     title = 'новости'
#
#     content = {
#         'title': title,
#         'css_file': 'style-gallery.css',
#     }
#
#     return render(request, 'mainapp/news.html', content)

# def team(request):
#
#     title = 'сотрудники'
#
#     content = {
#         'title': title,
#         'css_file': 'style-gallery.css',
#     }
#
#     return render(request, 'mainapp/team.html', content)

# def contacts(request):
#
#     title = 'контакты'
#
#     contact_data = Contacts.objects.get(pk=1)
#
#     content = {
#         'title': title,
#         'css_file': 'style-gallery.css',
#         'contact_data': contact_data,
#     }
#     return render(request, 'mainapp/contacts.html', content)

# def product(request, pk=None):
#
#     title = 'товары'
#
#     contact_data = Contacts.objects.get(pk=1)
#
#     game = get_object_or_404(Games, name=pk)
#     category = game.game_category
#     similar_games_list = list(Games.objects.filter(game_category=category).exclude(pk=game.pk))
#     result_list_similar = get_required_obj(similar_games_list, len(similar_games_list), 4)
#
#     content = {
#         'title': f'{title}: {game.name}',
#         'game': game,
#         'css_file': 'style-product-page.css',
#         'games': result_list_similar,
#         'contact_data': contact_data,
#     }
#     return render(request, 'mainapp/product.html', content)
