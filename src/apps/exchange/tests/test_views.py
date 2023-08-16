from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    
    def test_main_page(self):
        url = reverse('main_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)