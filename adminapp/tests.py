from django.test import TestCase
from django.test.client import Client


class TestAdminappTestCase(TestCase):
    expected_success_code = 200

    def setUp(self):
        self.client = Client()
        self.client.login(username='django', password='geekbrains')

    def test_adminapp_urls(self):
        response = self.client.get('/admin/users/read/1/')
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get('/admin/categories/read/1/')
        self.assertEqual(response.status_code, self.expected_success_code)

        response = self.client.get('/admin/orders/read/1/')
        self.assertEqual(response.status_code, self.expected_success_code)

