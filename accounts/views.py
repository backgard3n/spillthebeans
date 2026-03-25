# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reviews.models import DrinkReview, ShopReview


def auth_page(request):
    if request.method == "POST":
        if request.POST.get("form_type") == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect(request.GET.get("next", "home"))
            else:
                messages.error(request, "Invalid login")

        elif request.POST.get("form_type") == "register":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm = request.POST.get("confirm")

            if password != confirm:
                messages.error(request, "Passwords do not match")
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, "Account created. Please log in.")

    return render(request, "accounts/auth.html")


def logout_user(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    drink_reviews = (
        DrinkReview.objects.filter(user=request.user)
        .select_related("drink", "drink__shop")
        .order_by("-created_at")
    )
    shop_reviews = (
        ShopReview.objects.filter(user=request.user)
        .select_related("shop")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "drink_reviews": drink_reviews,
            "shop_reviews": shop_reviews,
        },
    )