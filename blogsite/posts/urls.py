from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.PostsIndexView.as_view(), name="index"),
    path("post/<int:pk>/", views.SeePost.as_view(), name="see_post"),
    path("comments/<int:pk>/", views.ShowPostComments.as_view(), name="show_comments"),
    path("comment/<int:pk>/", login_required(views.CommentPost.as_view()), name="post_comment"),
    path("comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("post/like/<int:pk>/", login_required(views.LikePost.as_view()), name="like_post"),
    path("post/this-like/<int:pk>/", login_required(views.LikePost.as_view()), name="this_like"),
    path("comment/comment-like/<int:pk>/", login_required(views.LikeComment.as_view()), name="comment_like"),
    path("comment/like/<int:pk>/", login_required(views.LikeComment.as_view()), name="like_comment")
]