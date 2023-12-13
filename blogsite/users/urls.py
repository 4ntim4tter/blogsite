from . import views
from django.urls import path
from posts import views as home_views

urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("register/", views.register_user, name="register_user"),
    path('create/', views.create_user, name="create_user"),
    path('authenticate/', views.auth_user, name="auth_user"),
    path('dash/', views.dash_user, name="dash_user"),
    path('logout/', views.logout_user, name="logout_user"),
    path('', home_views.PostsIndexView.as_view(), name="index")
]