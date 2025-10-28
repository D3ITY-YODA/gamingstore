from django.test import TestCase
from .models import Product, DigitalKey

class CatalogTests(TestCase):
    def test_product_creation(self):
        p = Product.objects.create(title='Test', price=10.00)
        self.assertEqual(str(p), 'Test (PC)')
