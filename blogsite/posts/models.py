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
        content_type = ContentType.objects.get_for_model(Post)
        likes = Like.objects.all().filter(object_id=self.pk, content_type=content_type).count()
        return likes

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=700)
    pub_date = models.DateField()

    def __str__(self):
        comment =  self.username.username + ": " + self.text.rstrip()
        return comment

    def likes(self):
        content_type = ContentType.objects.get_for_model(Comment)
        likes = Like.objects.all().filter(object_id=self.pk, content_type=content_type).count()
        return likes
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return f"{self.user.username} {self.content_object}"