from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, FloatField, F, ExpressionWrapper, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ShopForm
from .models import Shop



def shop_list(request):
    shops = (
        Shop.objects.filter(is_approved=True)
        .annotate(avg_rating=Avg("shop_reviews__overall_score"))
    )

    query = request.GET.get("q")
    min_rating = request.GET.get("rating")
    sort = request.GET.get("sort", "name")

    if query:
        shops = shops.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )

    if min_rating:
        try:
            shops = shops.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass

    if sort == "rating":
        shops = shops.order_by("-avg_rating", "name")
    else:
        shops = shops.order_by("name")

    return render(
        request,
        "shops/list.html",
        {
            "shops": shops,
            "query": query,
            "selected_rating": min_rating,
            "selected_sort": sort,
        },
    )


def shop_detail(request, slug):
    shop = get_object_or_404(Shop, slug=slug, is_approved=True)

    drinks = shop.drinks.all()
    shop_reviews = shop.shop_reviews.select_related("user").all()
    avg_shop_rating = shop_reviews.aggregate(avg=Avg("overall_score"))["avg"]

    return render(
        request,
        "shops/detail.html",
        {
            "shop": shop,
            "drinks": drinks,
            "shop_reviews": shop_reviews,
            "avg_shop_rating": avg_shop_rating,
        },
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
            return redirect("home")
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