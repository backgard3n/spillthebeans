from django.db.models import Avg, FloatField, F, ExpressionWrapper
from django.shortcuts import get_object_or_404, render

from shops.models import Shop
from .models import Drink


def drink_list(request):
    drinks = Drink.objects.select_related("shop").annotate(
        avg_taste=Avg("reviews__taste"),
        avg_temp=Avg("reviews__temperature"),
        avg_value=Avg("reviews__value"),
        avg_presentation=Avg("reviews__presentation"),
        avg_strength=Avg("reviews__strength"),
    ).annotate(
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

    shop_slug = request.GET.get("shop")
    category = request.GET.get("category")
    min_rating = request.GET.get("rating")

    if shop_slug:
        drinks = drinks.filter(shop__slug=shop_slug)

    if category:
        drinks = drinks.filter(category__iexact=category)

    if min_rating:
        try:
            drinks = drinks.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass

    shops = Shop.objects.filter(is_approved=True).order_by("name")

    return render(
        request,
        "drinks/list.html",
        {
            "drinks": drinks,
            "shops": shops,
            "selected_shop": shop_slug,
            "selected_category": category,
            "selected_rating": min_rating,
        },
    )


def drink_detail(request, slug):
    drink = get_object_or_404(
        Drink.objects.select_related("shop").prefetch_related("reviews", "reviews__user"),
        slug=slug,
    )

    reviews = drink.reviews.all().order_by("-created_at")

    return render(
        request,
        "drinks/detail.html",
        {
            "drink": drink,
            "reviews": reviews,
        },
    )