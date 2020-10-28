from django.conf import settings
from django.db import models

from mainapp.models import Games


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    DONE = 'DN'
    CANCEL = 'CNC'

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'обрабатывается'),
        (PROCEEDED, 'обработан'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (DONE, 'выдан'),
        (CANCEL, 'отменен')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.CharField(max_length=3, choices=ORDER_STATUSES,  verbose_name='Статус заказа')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Games, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def get_product_cost(self):
        return self.product.price * self.quantity
