from django.test import RequestFactory, TestCase
from django.urls import reverse

from posts.models import Post
from django.contrib.auth.models import User

# Create your tests here.
from django.test import Client

class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create(username='digimon22', password='232312')
        self.post = Post.objects.create(username=self.user, title="Post Title", text="This is the text of the post", pub_date="2024-01-25")

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

    def test_save_new(self):       
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('save_new'), data={'posttitle':'title', 'posttext':'texty'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('dash_user'))
    
    def test_save_post(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('save_post', kwargs={'pk':self.user.pk}), data={f'posttext{self.user.pk}':'newtext'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(pk=self.user.pk).text , 'newtext')

    def test_delete_post(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(reverse('delete_post', kwargs={'pk':self.user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(pk=self.user.pk).exists())