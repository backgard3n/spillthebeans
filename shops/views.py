from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

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
            shop.submitted_by = request.user
            shop.is_approved = False
            shop.save()
            messages.success(request, "Shop submitted! It will appear once approved.")
            return redirect("shops:shop_list")
    else:
        form = ShopForm()

    return render(request, "shops/add_shop.html", {"form": form})