from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.middleware import SessionMiddleware
import django.shortcuts
from django.test import RequestFactory, TestCase
from django.urls import reverse
from .views import logout_user

# Create your tests here.
from django.test import Client

class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create(username='digimon22', password='232312')

    def test_auth_user(self):
        response = self.client.post('/authenticate/', {'username':'digimon22', 'password':'232312'})
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        self.client.post('/create/', {'username':'createduser', 'password':'232312'})
        user = User.objects.get(username='createduser')
        self.assertEqual(user.username, 'createduser')

    def test_logout_user(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('logout_user'), follow=True)
        self.assertEqual(response.status_code, 200)               
        self.assertRedirects(response, reverse('index'))

    