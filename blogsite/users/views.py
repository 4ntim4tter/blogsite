from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def login_user(request):
    return render(request, 'users/login.html', {})

def register_user(request):
    return render(request, 'users/register.html', {})

def dash_user(request):
    return render(request, 'users/dash.html')

def create_user(request):
    print(User.objects.filter(username=request.POST['username']))
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
    

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect('index')