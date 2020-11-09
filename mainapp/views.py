import random
import time


from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.base import View, ContextMixin, TemplateView

from basketapp.models import Basket
from mainapp.models import Games, Contacts, DiscountGames, GameCategories


def get_hot_product():
    games_list = Games.objects.all().exclude(quantity=0)
    return random.sample(list(games_list), 1)[0]


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

    def get_queryset(self):
        game_list = list(Games.objects.all())
        result_list = get_required_obj(game_list, 4)
        return result_list

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'главная'
        context_data['css_file'] = 'style-index.css'
        context_data['contact_data'] = Contacts.objects.get(pk=1)
        return context_data


# def main(request, pk=None):
#
#     title = 'главная'
#
#     contact_data = Contacts.objects.get(pk=1)
#     game_list = list(Games.objects.all())
#     result_list = get_required_obj(game_list, 4)
#     content = {
#         'title': title,
#         'css_file': 'style-index.css',
#         'games': result_list,
#         'contact_data': contact_data,
#     }
#     return render(request, 'mainapp/index.html', content)


class AboutTemplateView(TemplateView):
    template_name = 'mainapp/about.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'о нас'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


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


class ServiceTemplateView(TemplateView):
    template_name = 'mainapp/services.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'услуги'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


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


class GalleryListView(ListView):
    model = Games
    template_name = 'adminapp/games_list.html'
    paginate_by = 4

    def get_queryset(self):
        global hot_product
        hot_product = get_hot_product()
        rest_games = Games.objects.all().exclude(pk=hot_product.pk)
        return rest_games

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'галлерея'
        context_data['css_file'] = 'style-gallery.css'
        context_data['hot_product'] = hot_product
        context_data['links_menu'] = GameCategories.objects.all()
        context_data['games_discount'] = DiscountGames.objects.all()
        return context_data


# def gallery(request, page=1):
#
#     title = 'галлерея'
#
#     links_menu = GameCategories.objects.all()
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
#         'page_obj': products_paginator,
#         'games_discount': result_list_discount,
#         'hot_product': get_hot_product()
#     }
#     return render(request, 'mainapp/games_list.html', content)


class ByCategoryListView(ListView):
    model = Games
    template_name = 'mainapp/games_by_category.html'
    paginate_by = 4

    def get_queryset(self):
        category_pk = self.kwargs.get('pk', None)
        games_by_category = Games.objects.filter(game_category=category_pk)
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
        context_data['hot_product'] = get_hot_product()
        context_data['games_discount'] = DiscountGames.objects.all()
        return context_data


# def by_category(request, pk, page=1):
#
#     title = 'категории'
#
#     links_menu = GameCategories.objects.all()
#     if pk == 0:
#         games_list = Games.objects.all()
#         category = {'name': 'все', 'pk': pk}
#     else:
#         category = get_object_or_404(GameCategories, pk=pk)
#         games_list = Games.objects.filter(game_category=category).order_by('name')
#
#     paginator = Paginator(games_list, 4)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#
#     content = {'title': title,
#                'css_file': 'style-gallery.css',
#                'links_menu': links_menu,
#                'games': products_paginator,
#                'hot_product': get_hot_product(),
#                'category': category,
#                }
#
#     return render(request, 'mainapp/games_by_category.html', content)


class NewsTemplateView(TemplateView):

    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'новости'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


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


class TeamTemplateView(TemplateView):
    template_name = 'mainapp/team.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'сотрудники'
        context_data['css_file'] = 'style-gallery.css'
        return context_data


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

class ContactsListView(ListView):
    model = Contacts
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contact_data'] = Contacts.objects.get(pk=1)
        context_data['title'] = 'контакты'
        context_data['css_file'] = 'style-gallery.css'
        return context_data

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


class ProductDetailView(DetailView):
    model = Games

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        game_pk = self.kwargs.get('pk', None)
        category = Games.objects.get(pk=game_pk).game_category.pk
        # context_data['game'] = Games.objects.get(pk=game_pk)
        context_data['object_list'] = Games.objects.filter(game_category=category).exclude(pk=game_pk).order_by('?').\
                                          select_related()[:4]

        context_data['title'] = 'товары'
        context_data['css_file'] = 'style-product-page.css'
        context_data['contact_data'] = Contacts.objects.get(pk=1)
        return context_data


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
