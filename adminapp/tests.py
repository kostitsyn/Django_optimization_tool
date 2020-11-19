from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from geekshop import settings
from mainapp.models import GameCategories, Games


class TestAdminappTestCase(TestCase):
    expected_success_code = 200

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.client.login(username='django', password='geekbrains')

    def test_adminapp_urls(self):

        response = self.client.get('/admin/users/create/')
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get('/admin/users/read/1/')
        self.assertEqual(response.status_code, self.expected_success_code)

        for user in ShopUser.objects.all():
            response = self.client.get(f'/admin/users/update/{user.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)

            response = self.client.get(f'/admin/users/delete/{user.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)


        response = self.client.get('/admin/categories/create/')
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get('/admin/categories/read/1/')
        self.assertEqual(response.status_code, self.expected_success_code)

        for category in GameCategories.objects.all():
            response = self.client.get(f'/admin/categories/update/{category.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)

            response = self.client.get(f'/admin/categories/delete/{category.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)


        for category in GameCategories.objects.all():
            response = self.client.get(f'/admin/products/create/category/{category.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)

            response = self.client.get(f'/admin/products/read/category/{category.pk}/1/')
            self.assertEqual(response.status_code, self.expected_success_code)

        for game in Games.objects.all():
            response = self.client.get(f'/admin/products/update/{game.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)

            response = self.client.get(f'/admin/products/delete/{game.pk}/')
            self.assertEqual(response.status_code, self.expected_success_code)


        response = self.client.get('/admin/orders/read/1/')
        self.assertEqual(response.status_code, self.expected_success_code)

        def tearDown(self):
            call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')