from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from posts.models import Post 
import datetime

# Create your views here.
def login_user(request):
    return render(request, 'users/login.html', {})

def register_user(request):
    return render(request, 'users/register.html', {})

@login_required
def dash_user(request):
    user_id = request.user.id
    posts = Post.objects.filter(username_id=f'{user_id}').order_by('-pub_date')
    paginated_posts = Paginator(posts, 5)
    selected_page = paginated_posts.get_page(request.GET.get('page'))
    if request.htmx:
        return render(request, 'snippets/user_posts.html', {'posts':selected_page})
    return render(request, 'users/dash.html', {'posts':selected_page})

def create_user(request):
    if User.objects.filter(username=request.POST['username']):
        messages.error(request, "User already exists.")
        return redirect(register_user)
    else:
        user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'])
        user.save()
        login(request, user)
        messages.success(request, "Registration Successful.")
        return redirect('index')
    
def auth_user(request):
    user = authenticate(request, 
                        username=request.POST['username'], 
                        password=request.POST['password'])
    if user is not None:
        login(request, user)
        messages.success(request, "Login Successful.")
        return redirect('index')
    else:
        messages.error(request, "Incorrect Credentials")
        return render(request, 'users/login.html')
    
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect('index')

@login_required
@require_http_methods(['DELETE'])
def delete_post(request, pk):
    post = Post.objects.all().filter(pk=pk)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('dash_user')

@login_required
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'snippets/edit_post.html', {'post':post})

@login_required
def cancel_edit(request, pk):
    post = Post.objects.get(pk=pk)
    messages.error(request, "Edit canceled.")
    return render(request, 'snippets/post_form.html', {'post':post})

@login_required
def save_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.text = request.POST[f'posttext{pk}']
    post.save()
    messages.info(request, "Post edited.")
    return render(request, 'snippets/post_form.html', {'post':post})

@login_required
def new_post(request):
    return render(request, 'snippets/new_post.html')

@login_required
def save_new(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    post = Post.objects.create(username=user, 
                               title=request.POST['posttitle'], 
                               text=request.POST['posttext'], 
                               pub_date=datetime.date.today())
    post.save()
    posts = Post.objects.filter(username_id=f'{user_id}').order_by('-pub_date')
    paginated_posts = Paginator(posts, 5)
    selected_page = paginated_posts.get_page(request.GET.get('page'))
    return render(request, 'snippets/user_posts.html', {'posts':selected_page})

@login_required
def cancel_new(request):
    return render(request, 'snippets/new_post_button.html')