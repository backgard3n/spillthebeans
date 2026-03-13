from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, FloatField, F, ExpressionWrapper
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ShopForm
from .models import Shop


def shop_list(request):
    sort = request.GET.get("sort", "name")

    shops = Shop.objects.filter(is_approved=True).annotate(
        avg_taste=Avg("drinks__reviews__taste"),
        avg_temp=Avg("drinks__reviews__temperature"),
        avg_value=Avg("drinks__reviews__value"),
        avg_presentation=Avg("drinks__reviews__presentation"),
        avg_strength=Avg("drinks__reviews__strength"),
    ).annotate(
        avg_rating=ExpressionWrapper(
            (
                F("avg_taste") +
                F("avg_temp") +
                F("avg_value") +
                F("avg_presentation") +
                F("avg_strength")
            ) / 5.0,
            output_field=FloatField(),
        )
    )

    if sort == "rating":
        shops = shops.order_by("-avg_rating", "name")
    else:
        shops = shops.order_by("name")

    return render(
        request,
        "shops/list.html",
        {
            "shops": shops,
            "selected_sort": sort,
        },
    )


def shop_detail(request, slug):
    shop = get_object_or_404(Shop, slug=slug, is_approved=True)

    drinks = shop.drinks.all().prefetch_related("reviews", "reviews__user")

    reviews = []
    for d in drinks:
        reviews.extend(list(d.reviews.all()))
    reviews.sort(key=lambda r: r.created_at, reverse=True)

    return render(
        request,
        "shops/detail.html",
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

    return render(
        request,
        "shops/edit.html",
        {
            "form": form,
            "shop": shop,
        },
    )