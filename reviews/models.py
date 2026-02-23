from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from drinks.models import Drink


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name="reviews")

    taste = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    strength = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    presentation = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "drink"], name="unique_review_per_user_per_drink")
        ]

    @property
    def overall(self) -> float:
        return (self.taste + self.strength + self.presentation + self.value) / 4.0

    def __str__(self):
        return f"Review by {self.user} on {self.drink}"