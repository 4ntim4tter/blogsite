from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Comment, Post

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
        return render(request, self.template_name, {'post':post})

class ShowPostComments(ListView):
    template_name = "snippets/comment.html"
    model = Comment

    def get(self, request, pk):
        comments = Comment.objects.all().filter(post=pk)
        return render(request, self.template_name, {'comments':comments})