from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def login_user(request):
    return render(request, 'users/login.html', {})

def register_user(request):
    return render(request, 'users/register.html', {})