import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Games, Contacts, DiscountGames, GameCategories


def get_hot_product():
    games_list = Games.objects.all()
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


def main(request, pk=None):

    title = 'главная'

    contact_data = Contacts.objects.get(pk=1)
    game_list = list(Games.objects.all())
    result_list = get_required_obj(game_list, 4)
    content = {
        'title': title,
        'name_page': 'historical games',
        'css_file': 'style-index.css',
        'games': result_list,
        'contact_data': contact_data,
    }
    return render(request, 'mainapp/index.html', content)


def about(request):

    title = 'о нас'

    content = {
        'title': title,
        'css_file': 'style-gallery.css',
    }

    return render(request, 'mainapp/about.html', content)


def service(request):

    title = 'услуги'

    content = {
        'title': title,
        'css_file': 'style-gallery.css',
    }

    return render(request, 'mainapp/services.html', content)


def gallery(request, page=1):

    title = 'галлерея'

    links_menu = GameCategories.objects.all()

    hot_product = get_hot_product()
    games_list = list(Games.objects.all().exclude(pk=hot_product.pk))

    game_discount = list(DiscountGames.objects.all())
    result_list_discount = get_required_obj(game_discount, 2)

    paginator = Paginator(games_list, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': title,
        'css_file': 'style-gallery.css',
        'links_menu': links_menu,
        'games': products_paginator,
        'games_discount': result_list_discount,
        'hot_product': get_hot_product()
    }
    return render(request, 'mainapp/gallery.html', content)


def by_category(request, pk, page=1):

    title = 'категории'

    links_menu = GameCategories.objects.all()
    if pk == 0:
        games_list = Games.objects.all()
        category = {'name': 'все', 'pk': pk}
    else:
        category = get_object_or_404(GameCategories, pk=pk)
        games_list = Games.objects.filter(game_category=category).order_by('name')

    paginator = Paginator(games_list, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {'title': title,
               'css_file': 'style-gallery.css',
               'links_menu': links_menu,
               'games': products_paginator,
               'hot_product': get_hot_product(),
               'category': category,
               }

    return render(request, 'mainapp/games_by_category.html', content)


def news(request):

    title = 'новости'

    content = {
        'title': title,
        'css_file': 'style-gallery.css',
    }

    return render(request, 'mainapp/news.html', content)


def team(request):

    title = 'сотрудники'

    content = {
        'title': title,
        'css_file': 'style-gallery.css',
    }

    return render(request, 'mainapp/team.html', content)


def contacts(request):

    title = 'контакты'

    contact_data = Contacts.objects.get(pk=1)

    content = {
        'title': title,
        'css_file': 'style-gallery.css',
        'contact_data': contact_data,
    }
    return render(request, 'mainapp/contacts.html', content)


def product(request, pk=None):

    title = 'товары'

    contact_data = Contacts.objects.get(pk=1)

    game = get_object_or_404(Games, name=pk)
    category = game.game_category
    similar_games_list = list(Games.objects.filter(game_category=category).exclude(pk=game.pk))
    result_list_similar = get_required_obj(similar_games_list, len(similar_games_list), 4)

    content = {
        'title': f'{title}: {game.name}',
        'game': game,
        'css_file': 'style-product-page.css',
        'games': result_list_similar,
        'contact_data': contact_data,
    }
    return render(request, 'mainapp/product.html', content)
