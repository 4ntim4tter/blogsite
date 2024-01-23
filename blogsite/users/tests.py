from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

# Create your tests here.
from django.test import Client

class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_auth_user(self):
        response = self.client.post('/authenticate/', {'username':'sarmica', 'password':'123321'})
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        self.client.post('/create/', {'username':'digimon22', 'password':'232312'})
        user = User.objects.get(username='digimon22')
        self.assertEqual(user.username, 'digimon22')

    