from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import ShopForm
from .models import Shop


def shop_list(request):
    shops = Shop.objects.filter(is_approved=True)
    return render(request, "shops/shop_list.html", {"shops": shops})


def shop_detail(request, slug):
    shop = get_object_or_404(Shop, slug=slug, is_approved=True)

    drinks = shop.drinks.all().prefetch_related("reviews", "reviews__user")

    # Flatten reviews across all drinks (simple approach)
    reviews = []
    for d in drinks:
        reviews.extend(list(d.reviews.all()))
    reviews.sort(key=lambda r: r.created_at, reverse=True)

    return render(
        request,
        "shops/shop_detail.html",
        {"shop": shop, "drinks": drinks, "reviews": reviews},
    )


@login_required
def add_shop(request):
    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.submitted_by = request.user
            shop.is_approved = False
            shop.save()
            messages.success(request, "Shop submitted for approval.")
            return redirect("shops:detail", slug=shop.slug)
    else:
        form = ShopForm()

    return render(request, "shops/add.html", {"form": form})


@login_required
def edit_shop(request, slug):
    shop = get_object_or_404(Shop, slug=slug)

    if shop.owner != request.user:
        return HttpResponseForbidden("You do not own this shop.")

    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            updated_shop = form.save(commit=False)
            updated_shop.is_approved = False
            updated_shop.save()
            messages.success(request, "Shop updated and resubmitted for approval.")
            return redirect("shops:detail", slug=shop.slug)
    else:
        form = ShopForm(instance=shop)

    return render(request, "shops/edit.html", {
        "form": form,
        "shop": shop,
    })