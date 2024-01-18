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
    
    def create_links(self, text:str):
        links = []
        if "youtube.com/watch" in text:
            links = text.split(' ')
        elif "youtu.be/" in text:
            links = text.split(' ')
        else:
            return None

        for index, link  in enumerate(links):
            if "youtube.com/watch" in link:
                links[index] = f"<a href={link}>{link}</a>"
                video_code = link.split('=')[1].split('&')[0]
                embeded_link = f"<iframe src='http://www.youtube.com/embed/{video_code}' style='width:560px; height:316px'frameborder='0' allowfullscreen></iframe>"
                new_link = Link(post=self, link=embeded_link)
                new_link.save()
            elif "youtu.be/" in link:
                links[index] = f"<a href={link}>{link}</a>"
                video_code = link.split('/')[-1].split('&')[0]
                embeded_link = f"<iframe src='http://www.youtube.com/embed/{video_code}' style='width:560px; height:316px'frameborder='0' allowfullscreen></iframe>"
                new_link = Link(post=self, link=embeded_link)
                new_link.save()
        
        return ' '.join(links)

    def get_links(self):
        links = Link.objects.all().filter(post=self)
        return links


class Link(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    link = models.TextField(max_length=1000)


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