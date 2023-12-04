from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostsIndexView.as_view(), name="index")
]