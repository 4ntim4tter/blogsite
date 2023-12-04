from django.views.generic import ListView

from .models import Post

class PostsIndexView(ListView):
    template_name = "posts/index.html"
    context_object_name = "latest_posts_list"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')