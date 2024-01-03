from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostsIndexView.as_view(), name="index"),
    path("post/<int:pk>/", views.SeePost.as_view(), name="see_post"),
    path("comments/<int:pk>/", views.ShowPostComments.as_view(), name="show_comments"),
    path("comment/<int:pk>/", views.CommentPost.as_view(), name="post_comment"),
    path("comment/<int:pk>/delete", views.DeletePost.as_view(), name="delete_comment")
]