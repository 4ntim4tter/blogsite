import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DeleteView
from django.contrib import messages

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
        comments = Comment.objects.all().filter(post=pk).order_by('-pub_date', '-id')
        return render(request, self.template_name, {'comments':comments})
    
class CommentPost(ListView):
    template_name = "snippets/comment.html"
    login_required = True
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

class DeletePost(DeleteView):
    template_name = "snippets/comment.html"
    login_required = True
    http_method_names = ["delete"]
    model = Comment

    def delete(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        post_id = comment.post.id
        comment.delete()
        messages.success(request, "Comment Deleted.")
        return redirect('show_comments', pk=post_id)