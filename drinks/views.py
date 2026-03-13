from django.db.models import Avg, FloatField, F, ExpressionWrapper, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shops.models import Shop
from .forms import DrinkForm
from .models import Drink


def drink_list(request):
    drinks = (
        Drink.objects.select_related("shop")
        .filter(shop__is_approved=True)
        .annotate(
            avg_taste=Avg("drink_reviews__taste"),
            avg_temp=Avg("drink_reviews__temperature"),
            avg_value=Avg("drink_reviews__value"),
            avg_presentation=Avg("drink_reviews__presentation"),
            avg_strength=Avg("drink_reviews__strength"),
        )
        .annotate(
            avg_rating=ExpressionWrapper(
                (
                    F("avg_taste")
                    + F("avg_temp")
                    + F("avg_value")
                    + F("avg_presentation")
                    + F("avg_strength")
                ) / 5.0,
                output_field=FloatField(),
            )
        )
    )

    shop_slug = request.GET.get("shop")
    drink_type = request.GET.get("drink_type")
    min_rating = request.GET.get("rating")
    query = request.GET.get("q")
    sort = request.GET.get("sort", "name")

    if shop_slug:
        drinks = drinks.filter(shop__slug=shop_slug)

    if drink_type:
        drinks = drinks.filter(drink_type=drink_type)

    if min_rating:
        try:
            drinks = drinks.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass

    if query:
        drinks = drinks.filter(
            Q(name__icontains=query) | Q(shop__name__icontains=query)
        )

    if sort == "top_rated":
        drinks = drinks.order_by("-avg_rating", "name")
    elif sort == "price_low":
        drinks = drinks.order_by("price", "name")
    elif sort == "price_high":
        drinks = drinks.order_by("-price", "name")
    else:
        drinks = drinks.order_by("name")

    shops = Shop.objects.filter(is_approved=True).order_by("name")

    return render(
        request,
        "drinks/list.html",
        {
            "drinks": drinks,
            "shops": shops,
            "selected_shop": shop_slug,
            "selected_drink_type": drink_type,
            "selected_rating": min_rating,
            "query": query,
            "selected_sort": sort,
        },
    )


def drink_detail(request, slug):
    drink = get_object_or_404(
        Drink.objects.select_related("shop").filter(shop__is_approved=True),
        slug=slug,
    )

    reviews = drink.drink_reviews.select_related("user").all()

    overall = (
        reviews.aggregate(
            avg_taste=Avg("taste"),
            avg_temp=Avg("temperature"),
            avg_value=Avg("value"),
            avg_presentation=Avg("presentation"),
            avg_strength=Avg("strength"),
        )
    )

    scores = [
        overall["avg_taste"],
        overall["avg_temp"],
        overall["avg_value"],
        overall["avg_presentation"],
        overall["avg_strength"],
    ]
    scores = [s for s in scores if s is not None]
    overall_score = round(sum(scores) / len(scores), 1) if scores else None

    return render(
        request,
        "drinks/detail.html",
        {
            "drink": drink,
            "reviews": reviews,
            "overall": overall_score,
        },
    )


@login_required
def add_drink(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug, is_approved=True)

    if shop.owner != request.user and not request.user.is_staff:
        messages.error(request, "Only the shop owner can add drinks.")
        return redirect("shops:detail", slug=shop.slug)

    if request.method == "POST":
        form = DrinkForm(request.POST, request.FILES)
        if form.is_valid():
            drink = form.save(commit=False)
            drink.shop = shop
            drink.save()
            messages.success(request, "Drink added successfully.")
            return redirect("drinks:detail", slug=drink.slug)
    else:
        form = DrinkForm()

    return render(request, "drinks/add.html", {"form": form, "shop": shop})