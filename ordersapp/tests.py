from django.core.management import call_command
from django.test import TestCase

from authapp.models import ShopUser
from mainapp.models import Games
from ordersapp.models import Order, OrderItem


class OrdersTestCase(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        user = ShopUser.objects.get(username='django')
        order = Order.objects.create(user=user)
        product_1 = Games.objects.get(pk=8)
        product_2 = Games.objects.get(pk=13)
        self.order_item_1 = OrderItem.objects.create(order=order,
                                                     product=product_1,
                                                     quantity=10)

        self.order_item_2 = OrderItem.objects.create(order=order,
                                                     product=product_2,
                                                     quantity=15)

    def test_order_item_get(self):
        order_item_1 = OrderItem.objects.get(product__name='АSASSIN’S CREED: Rogue')
        order_item_2 = OrderItem.objects.get(product__name='RYSE: Son Of Rome')
        self.assertEqual(order_item_1, self.order_item_1)
        self.assertEqual(order_item_2, self.order_item_2)

    def test_get_order_item(self):
        order_item_1 = OrderItem.objects.get(product__name='АSASSIN’S CREED: Rogue')
        order_item = OrderItem.get_item(pk=self.order_item_1.pk)

        self.assertEqual(order_item_1, order_item)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',\
                     'basketapp')
