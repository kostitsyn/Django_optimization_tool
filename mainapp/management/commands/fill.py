import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import Games, Contacts, GameCategories, DiscountGames

FILE_PATH = os.path.join(settings.BASE_DIR, 'mainapp/json')

def load_from_json(file_name):
    with open(os.path.join(FILE_PATH, f"{file_name}.json"), encoding='utf-8') as json_file:
        return json.load(json_file)



class Command(BaseCommand):

    def handle(self, *args, **options):


        categories = load_from_json("categories")
        Games.objects.all().delete()
        GameCategories.objects.all().delete()
        for category in categories:
            GameCategories.objects.create(**category)

        games = load_from_json("games")
        for game in games:
            game_cat = game['game_category']
            _category = GameCategories.objects.get(name=game_cat)
            game['game_category'] = _category
            Games.objects.create(**game)

        games_discount = load_from_json("games_discount")
        DiscountGames.objects.all().delete()
        for game_disc in games_discount:
            game_cat = game_disc['game_category']
            _category = GameCategories.objects.get(name=game_cat)
            game_disc['game_category'] = _category
            DiscountGames.objects.create(**game_disc)

        contacts = load_from_json("contacts")
        Contacts.objects.all().delete()
        for contact in contacts:
            Contacts.objects.create(**contact)

        ShopUser.objects.create_superuser(username='django', email=None, password='geekbrains', age=30)

