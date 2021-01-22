from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

# Основное тестирование сделал для adminapp

class TestAdminappTestCase(TestCase):
    expected_success_code = 200

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.expected_success_code)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',\
                     'basketapp')



