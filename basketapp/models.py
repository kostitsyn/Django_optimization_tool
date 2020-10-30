from django.conf import settings
from django.db import models

from mainapp.models import Games


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Games, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-add_datetime']

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user)

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity

    @property
    def get_total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def get_total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        print('hello')
        print(_items)
        _total_cost = sum(list(map(lambda x: x.get_product_cost, _items)))
        return _total_cost


