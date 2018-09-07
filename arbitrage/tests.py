from django.urls import reverse, resolve
from django.test import TestCase
from .views import contact, blockfolio 

class ArbitrageTests(TestCase):
    def setUp(self):
        url = reverse('contact')
        self.response = self.client.get(url)

    def test_arbitrage_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_arbitrage_url_resolves_contact_view(self): # change view name
        view = resolve('/')
        self.assertEqual(view.func, contact)

class BlockfolioTests(TestCase):
    def setUp(self):
        url = reverse('blockfolio')
        self.response = self.client.get(url)

    def test_blockfolio_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/blockfolio')
        self.assertEqual(view.func, blockfolio)