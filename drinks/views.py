from django.shortcuts import render, get_object_or_404
from .models import Drink

def drink_list(request):
    drinks = Drink.objects.all()
    return render(request, "drinks/list.html", {"drinks": drinks})

def drink_detail(request, slug):
    drink = get_object_or_404(Drink, slug=slug)
    return render(request, "drinks/detail.html", {"drink": drink})

def leaderboard(request):
    # simple placeholder for now (we’ll add ORM aggregation next)
    drinks = Drink.objects.all()
    return render(request, "drinks/leaderboard.html", {"drinks": drinks})