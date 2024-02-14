import datetime
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
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
                                             pub_date=datetime.date.today(),
                                             likes_count=0)
        new_comment.save()
        post.comments_count += 1
        post.save()
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
            this_like = Like(user=request.user, content_type=content_type, object_id=pk)
            this_like.save()
            liked_post.likes_count += 1
            liked_post.save()
            return render(request, self.template_name, {'post':liked_post, 'this_like':this_like})
        else:
            this_like = this_like[0]
            this_like.delete()
            liked_post.likes_count -= 1
            liked_post.save()
            this_like = None
            return render(request, self.template_name, {'post':liked_post, 'this_like':this_like})

    def get(self, request, pk):
        this_like = Like.objects.all().filter(object_id=pk, user=request.user)
        post = Post.objects.get(pk=pk)
        return render(request, self.template_name, {'post':post, 'this_like':this_like})

class LikeComment(ListView):
    template_name = "snippets/like_button2.html"
    http_method_names = ["post", "get"]
    model = Like

    def post(self, request, pk):
        this_like = Like.objects.all().filter(object_id=pk, user=request.user)
        comment = Comment.objects.get(pk=pk)
        content_type = ContentType.objects.get_for_model(Comment)
        if this_like.count() == 0:
            this_like = Like(user=request.user, content_type=content_type, object_id=pk)
            this_like.save()
            comment.likes_count += 1
            comment.save()
            return render(request, self.template_name, {'comment':comment, 'comment_like':this_like})
        else:
            this_like = this_like[0]
            this_like.delete()
            comment.likes_count -= 1
            comment.save()
            this_like = None
            return render(request, self.template_name, {'comment':comment, 'comment_like':this_like})
        
    def get(self, request, pk):
        comment_like = Like.objects.all().filter(object_id=pk, user=request.user)
        comment = Comment.objects.get(pk=pk)
        return render(request, self.template_name, {'comment':comment, 'comment_like':comment_like})

@login_required
@require_http_methods(['DELETE'])
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post_id = comment.post.id
    comment.delete()
    comments = Comment.objects.all().filter(post=post_id).order_by('-pub_date', '-id')
    messages.success(request, "Comment Deleted.")
    return render(request, 'snippets/comment.html', {'comments':comments})
