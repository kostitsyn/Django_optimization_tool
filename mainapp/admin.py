from django.contrib import admin

from mainapp.models import GameCategories, Games, Contacts, DiscountGames

admin.site.register(GameCategories)
admin.site.register(Games)
admin.site.register(Contacts)
admin.site.register(DiscountGames)
