    from django.test import TestCase
    from apps.catalog.models import Product, DigitalKey

class OrdersTests(TestCase):
    def test_quick_buy_assigns_key(self):
        p = Product.objects.create(title='QB Test', price=5.00)
        k = DigitalKey.objects.create(product=p, key='ABC-123')
        resp = self.client.post(f'/orders/quick-buy/{p.id}/', {'email': 'a@b.com'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('key', data)
        k.refresh_from_db()
        self.assertTrue(k.assigned)
