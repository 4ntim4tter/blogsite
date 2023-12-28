from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .models import Post

class PostsIndexView(ListView):
    template_name = "posts/index.html"
    context_object_name = "latest_posts_list"
    model = Post
    paginate_by = 3

    def get_template_names(self):
        if self.request.htmx:
            return 'snippets/load_on_scroll.html'
        return self.template_name

    def get_queryset(self):
        return Post.objects.order_by('-pub_date', '-id')

class SeePost(ListView):
    template_name = "posts/see_post.html"
    context_object_name = "post"
    model = Post

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(request, 'posts/see_post.html', {'post':post})
