import datetime
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.utils import get_model_from_relation
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Comment, Like, Post

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
        comments = Comment.objects.all().filter(post=pk).order_by('-pub_date', '-id')
        return render(request, self.template_name, {'comments':comments})
    
class CommentPost(ListView):
    template_name = "snippets/comment.html"
    http_method_names = ["post"]
    model = Comment

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        new_comment = Comment.objects.create(username=user, 
                                             post=post, 
                                             text=request.POST['new-comment-area'], 
                                             pub_date=datetime.date.today())
        new_comment.save()
        messages.success(request, "Commented Successfuly.")
        return redirect('show_comments', pk=pk)

class LikePost(ListView):
    template_name = "snippets/like_button.html"
    http_method_names = ["post", "get"]
    model = Like

    def post(self, request, pk):
        this_like = Like.objects.all().filter(object_id=pk, user=request.user)
        liked_post = Post.objects.get(pk=pk)
        content_type = ContentType.objects.get_for_model(Post)
        if this_like.count() == 0:
            this_like = Like(liked=True, user=request.user, content_type=content_type, object_id=pk)
            this_like.save()
            print("if",this_like.liked)
        elif this_like[0].liked:
            this_like = this_like[0]
            this_like.liked=False
            this_like.save()
            print("elif", this_like.liked)
        else:
            this_like = this_like[0]
            this_like.liked=True
            this_like.save()
            print("else", this_like.liked)
        return render(request, 'snippets/like_button.html', {'post':liked_post, 'this_like':this_like})

@login_required
@require_http_methods(['DELETE'])
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post_id = comment.post.id
    comment.delete()
    comments = Comment.objects.all().filter(post=post_id).order_by('-pub_date', '-id')
    messages.success(request, "Comment Deleted.")
    return render(request, 'snippets/comment.html', {'comments':comments})
