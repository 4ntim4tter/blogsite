from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostsIndexView.as_view(), name="index"),
    path("post/<int:pk>/", views.SeePost.as_view(), name="see_post")
]