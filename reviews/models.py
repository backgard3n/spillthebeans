from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey("drinks.Drink", on_delete=models.CASCADE, related_name="reviews")

    taste = models.PositiveSmallIntegerField(default=1)
    temperature = models.PositiveSmallIntegerField(default=1)
    value = models.PositiveSmallIntegerField(default=1)
    presentation = models.PositiveSmallIntegerField(default=1)
    strength = models.PositiveSmallIntegerField(default=1)

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "drink")

    @property
    def overall(self):
        return round(
            (
                self.taste +
                self.temperature +
                self.value +
                self.presentation +
                self.strength
            ) / 5,
            1
        )

    def __str__(self):
        return f"{self.user.username} review of {self.drink.name}"