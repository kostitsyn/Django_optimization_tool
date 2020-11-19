from django.test import TestCase
from django.test.client import Client


class TestAdminappTestCase(TestCase):
    expected_success_code = 200

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='geekbrains')

    # def test_mainapp_urls(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, self.expected_success_code)
    #
    #     response =
