from django.test import TestCase

# Create your tests here.
from django.test import Client

class TestViews(TestCase):
    def test_auth_user(self):
        client = Client()
        response = client.post('/authenticate/', {'username':'sarmica', 'password':'123321'})
        self.assertEqual(response.status_code, 200)