from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def login_user(request):
    return render(request, 'users/login.html', {})

def register_user(request):
    return render(request, 'users/register.html', {})

def create_user(request):
    user = User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password'])
    user.save()
    return HttpResponse(request.POST['username'])