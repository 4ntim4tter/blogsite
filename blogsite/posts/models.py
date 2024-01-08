from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    
    def comment_number(self):
        return self.comment_set.count()

    def likes(self):
        return self.objects.annotate(num_of_likes=models.Count())

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=700)
    pub_date = models.DateField()

    def __str__(self):
        comment =  self.username.username + ": " + self.text.rstrip()
        return comment

class Like(models.Model):
    liked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField(unique=True)
    content_object = GenericForeignKey("content_type", "object_id")