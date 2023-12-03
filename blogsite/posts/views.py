from django.shortcuts import render

from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-pub_date')[:2]
    return render(request, "posts/index.html", {"posts":posts})