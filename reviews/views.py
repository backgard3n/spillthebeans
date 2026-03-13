from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from drinks.models import Drink
from shops.models import Shop
from .forms import DrinkReviewForm, ShopReviewForm
from .models import DrinkReview, ShopReview


@login_required
def add_drink_review(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id, shop__is_approved=True)

    review, _ = DrinkReview.objects.get_or_create(
        user=request.user,
        drink=drink,
        defaults={
            "taste": 3,
            "temperature": 3,
            "strength": 3,
            "presentation": 3,
            "value": 3,
        },
    )

    if request.method == "POST":
        form = DrinkReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("drinks:detail", slug=drink.slug)
    else:
        form = DrinkReviewForm(instance=review)

    return render(
        request,
        "reviews/add_drink_review.html",
        {"form": form, "drink": drink},
    )


@login_required
def add_shop_review(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug, is_approved=True)

    review, _ = ShopReview.objects.get_or_create(
        user=request.user,
        shop=shop,
        defaults={"overall_score": 3},
    )

    if request.method == "POST":
        form = ShopReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("shops:detail", slug=shop.slug)
    else:
        form = ShopReviewForm(instance=review)

    return render(
        request,
        "reviews/add_shop_review.html",
        {"form": form, "shop": shop},
    )