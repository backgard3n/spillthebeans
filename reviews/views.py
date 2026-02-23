from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from drinks.models import Drink
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id)

    review, _created = Review.objects.get_or_create(
        user=request.user,
        drink=drink,
        defaults={"taste": 3, "strength": 3, "presentation": 3, "value": 3},
    )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("drinks:detail", slug=drink.slug)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/add.html", {"form": form, "drink": drink})