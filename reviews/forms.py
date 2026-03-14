from django import forms
from .models import DrinkReview, ShopReview


class DrinkReviewForm(forms.ModelForm):
    class Meta:
        model = DrinkReview
        fields = ["taste", "temperature", "strength", "presentation", "value", "comment"]


class ShopReviewForm(forms.ModelForm):
    class Meta:
        model = ShopReview
        fields = ["overall_score", "review_text"]