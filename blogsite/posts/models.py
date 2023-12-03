from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)
    pub_date = models.DateField()

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=700)
    pub_date = models.DateField()

    def __str__(self):
        return self.username.username + ":" + self.text[:20] + "..."
    