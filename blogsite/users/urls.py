from . import views
from django.urls import path
from posts import views as home_views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('create/', views.create_user, name='create_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('get_recovery_email/', views.get_recovery_email, name='get_recovery_email'),
    path('recover_account/', views.recover_account, name='recover_account'),
    path('authenticate/', views.auth_user, name='auth_user'),
    path('user_profile/<int:pk>/', views.user_profile, name='user_profile'),
    path('dash/', views.dash_user, name='dash_user'),
    path('new_post/', views.new_post, name='new_post'),
    path('save_new/', views.save_new, name='save_new'),
    path('cancel_new/', views.cancel_new, name='cancel_new'),
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
    path('cancel_edit/<int:pk>/', views.cancel_edit, name='cancel_edit'),
    path('save_edit/<int:pk>/', views.save_post, name='save_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('logout/', views.logout_user, name='logout_user'),
    path('', home_views.PostsIndexView.as_view(), name='index')
]