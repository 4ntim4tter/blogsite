from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from posts.models import Post 

# Create your views here.
def login_user(request):
    return render(request, 'users/login.html', {})

def register_user(request):
    return render(request, 'users/register.html', {})

@login_required
def dash_user(request):
    user_id = request.user.id
    posts = Post.objects.filter(username_id=f'{user_id}').order_by('-pub_date')
    if request.htmx:
        return render(request, 'snippets/user_posts.html', {'posts':posts})
    return render(request, 'users/dash.html', {'posts':posts})

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
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
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
def edit_post(request, pk):
    return redirect('index')

@login_required
@require_http_methods(['DELETE'])
def delete_post(request, pk):
    post = Post.objects.all().filter(pk=pk)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('dash_user')

