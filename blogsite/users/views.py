from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Sum
from django.http import response
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from posts.models import Post, Comment
import datetime


# Create your views here.
def login_user(request):
    return render(request, "users/login.html", {})


def register_user(request):
    return render(request, "users/register.html", {})


@login_required
def dash_user(request):
    user_id = request.user.id
    posts = Post.objects.filter(username_id=f"{user_id}").order_by("-pub_date", "-id")
    paginated_posts = Paginator(posts, 3)
    selected_page = paginated_posts.get_page(request.GET.get("page"))
    if request.htmx:
        return render(request, "snippets/user_posts.html", {"posts": selected_page})
    return render(request, "users/dash.html", {"posts": selected_page})


def check_username(request):
    search_term = request.GET['username']
    exists = User.objects.filter(username__iexact=search_term).exists()
    return render(request, 'snippets/username_checker.html', {'exists':exists, 'username':search_term})

def create_user(request):
    if User.objects.filter(username=request.POST["username"]).exists():
        messages.error(request, "User already exists.")
        return redirect(register_user)
    elif (
        validate_email(request.POST["email"])
        or User.objects.filter(email=request.POST["email"]).exists()
    ):
        messages.error(request, "Invalid e-mail or already exists.")
        return redirect(register_user)
    else:
        user = User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
            email=request.POST["email"],
        )
        user.is_active = False
        user.save()
        token = PasswordResetTokenGenerator().make_token(user)
        send_mail(
            "Forgotten Password",
            f"This is your activation link: http://127.0.0.1:8000/activate_account?token={token}&email={user.email}",
            "me@me.com",
            [user.email],
            fail_silently=False,
        )
        messages.success(
            request,
            "Registration Successful.\n Please check your inbox\nfor your verification e-mail.",
        )
        return redirect("index")


def activate_user(request):
    user = User.objects.get(email=request.GET.get("email"))
    if PasswordResetTokenGenerator().check_token(user, request.GET.get("token")):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account is now activated.")
        return redirect("index")
    else:
        return response.HttpResponse("Token expired.")


def forgot_password(request):
    return render(request, "users/forgot_password.html")


def get_recovery_email(request):
    email = request.POST["email"]
    exists = User.objects.filter(email=email).exists()
    if not exists:
        messages.error(request, "E-mail does not exist.")
        return render(request, "users/forgot_password.html")

    user = User.objects.get(email=email)
    if user.is_active:
        token = PasswordResetTokenGenerator().make_token(user)
        send_mail(
            "Forgotten Password",
            f"This is your password reset link: http://127.0.0.1:8000/recover_account?token={token}&email={email}",
            "me@me.com",
            [email],
            fail_silently=False,
        )
        return render(request, "snippets/email_sent.html")
    else:
        token = PasswordResetTokenGenerator().make_token(user)
        send_mail(
            "Forgotten Password",
            f"This is your password reset link: http://127.0.0.1:8000/activate_account?token={token}&email={email}",
            "me@me.com",
            [email],
            fail_silently=False,
        )
        return render(request, "snippets/email_sent.html")


def recover_account(request):
    email = request.GET.get("email")
    user = User.objects.get(email=email)
    if PasswordResetTokenGenerator().check_token(user, request.GET.get("token")):
        return redirect(password_change)
    else:
        return response.HttpResponse("Token Invalid")


def password_change(request):
    return render(request, "users/change_password.html")


def auth_user(request):
    user = User.objects.get(username=request.POST["username"])
    if user is None:
        messages.error(request, "Incorrect Credentials")
        return render(request, "users/login.html")

    if user.is_active:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        login(request, user)
        messages.success(request, "Login Successful.")
        return redirect("index")
    else:
        return render(request, "users/resend_verification.html", {"user": user})


def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    liked_posts = Post.objects.filter(username=user.pk).aggregate(Sum("likes_count"))[
        "likes_count__sum"
    ]
    liked_comments = Comment.objects.filter(username=user.pk).aggregate(
        Sum("likes_count")
    )["likes_count__sum"]
    latest_posts = Post.objects.filter(username=user.pk).order_by("-pub_date")[:5]
    top_posts = Post.objects.filter(username=user.pk).order_by("-likes_count")[:5]
    latest_comments = Comment.objects.filter(username=user.pk).order_by("-pub_date")[:5]
    top_comments = Comment.objects.filter(username=user.pk).order_by("-likes_count")[:5]
    return render(
        request,
        "users/profile.html",
        {
            "username": user.username,
            "latest_posts": latest_posts,
            "top_posts": top_posts,
            "latest_comments": latest_comments,
            "top_comments": top_comments,
            "liked_posts": liked_posts,
            "liked_comments": liked_comments,
        },
    )


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect("index")


@login_required
@require_http_methods(["DELETE"])
def delete_post(request, pk):
    post = Post.objects.all().filter(pk=pk)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect("dash_user")


@login_required
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, "snippets/edit_post.html", {"post": post})


@login_required
def cancel_edit(request, pk):
    post = Post.objects.get(pk=pk)
    messages.error(request, "Edit canceled.")
    return render(request, "snippets/post_form.html", {"post": post})


@login_required
def save_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.text = request.POST[f"posttext{pk}"]
    post.save()
    messages.info(request, "Post edited.")
    return render(request, "snippets/post_form.html", {"post": post})


@login_required
def new_post(request):
    return render(request, "snippets/new_post.html")


@login_required
def save_new(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    post = Post.objects.create(
        username=user,
        title=request.POST["posttitle"],
        text=request.POST["posttext"],
        pub_date=datetime.date.today(),
        likes_count=0,
        comments_count=0,
    )
    post.text = post.create_links(request.POST["posttext"])
    post.save()
    messages.success(request, "Post Saved")
    return redirect("dash_user")


@login_required
def cancel_new(request):
    return render(request, "snippets/new_post_button.html")
