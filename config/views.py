from django.db.models import Avg, FloatField, F, ExpressionWrapper, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render

from shops.models import Shop
from drinks.models import Drink


def home(request):
    top_shops = (
        Shop.objects.filter(is_approved=True)
        .annotate(
            avg_rating=Coalesce(
                Avg("shop_reviews__overall_score"),
                Value(0.0),
                output_field=FloatField(),
            )
        )
        .order_by("-avg_rating", "name")[:5]
    )

    top_drinks = (
        Drink.objects.select_related("shop")
        .filter(shop__is_approved=True)
        .annotate(
            avg_taste=Coalesce(Avg("drink_reviews__taste"), Value(0.0), output_field=FloatField()),
            avg_temp=Coalesce(Avg("drink_reviews__temperature"), Value(0.0), output_field=FloatField()),
            avg_value=Coalesce(Avg("drink_reviews__value"), Value(0.0), output_field=FloatField()),
            avg_presentation=Coalesce(Avg("drink_reviews__presentation"), Value(0.0), output_field=FloatField()),
            avg_strength=Coalesce(Avg("drink_reviews__strength"), Value(0.0), output_field=FloatField()),
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
        .order_by("-avg_rating", "name")[:6]
    )

    return render(
        request,
        "home.html",
        {
            "top_shops": top_shops,
            "top_drinks": top_drinks,
        },
    )