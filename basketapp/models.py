from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Games


# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Games, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-add_datetime']


    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    # @staticmethod
    # def get_items(user):
    #     # return Basket.objects.filter(user=user)
    #     return Basket.objects.filter(user=user).select_related()

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_total_quantity_cached(self):
        # _items = Basket.objects.filter(user=self.user)
        # _items = Basket.objects.filter(user=self.user).select_related()
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    # @property
    # def get_total_quantity(self):
    #     # _items = Basket.objects.filter(user=self.user)
    #     _items = Basket.objects.filter(user=self.user).select_related()
    #     _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
    #     return _total_quantity

    @cached_property
    def get_total_cost_cached(self):
        # _items = Basket.objects.filter(user=self.user)
        # _items = Basket.objects.filter(user=self.user).select_related()
        _items = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.get_product_cost, _items)))
        return _total_cost

    # @property
    # def get_total_cost(self):
    #     # _items = Basket.objects.filter(user=self.user)
    #     _items = Basket.objects.filter(user=self.user).select_related()
    #     _total_cost = sum(list(map(lambda x: x.get_product_cost, _items)))
    #     return _total_cost

    # def get_product_quantity(self, user):
    #     basket_items = self.get_items_cached
    #     basket_items_dic = {}
    #     [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]
    #     return basket_items_dic

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(*args, **kwargs)


