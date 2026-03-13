from django.conf import settings
from django.db import models


class DrinkReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    drink = models.ForeignKey(
        "drinks.Drink",
        on_delete=models.CASCADE,
        related_name="drink_reviews",
    )

    taste = models.PositiveSmallIntegerField(default=1)
    temperature = models.PositiveSmallIntegerField(default=1)
    value = models.PositiveSmallIntegerField(default=1)
    presentation = models.PositiveSmallIntegerField(default=1)
    strength = models.PositiveSmallIntegerField(default=1)

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "drink")
        ordering = ["-created_at"]

    @property
    def overall(self):
        return round(
            (
                self.taste
                + self.temperature
                + self.value
                + self.presentation
                + self.strength
            ) / 5,
            1,
        )

    def __str__(self):
        return f"{self.user} -> {self.drink}"


class ShopReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey(
        "shops.Shop",
        on_delete=models.CASCADE,
        related_name="shop_reviews",
    )
    overall_score = models.PositiveSmallIntegerField(default=1)
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "shop")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.shop}"