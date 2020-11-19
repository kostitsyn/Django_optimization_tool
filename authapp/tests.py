from django.test import TestCase
from django.core.management import call_command
from django.test.client import Client

from authapp.models import ShopUser


class TestUserManagement(TestCase):
    expected_success_code = 200
    expected_redirect_code = 302

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.user = ShopUser.objects.get(username='django')

    def test_user_login(self):
        self.client.login(username='django', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

    def test_basket_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, self.expected_redirect_code)
        self.assertEqual(response.url, '/auth/login/?next=/basket/')

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',\
                     'basketapp')

