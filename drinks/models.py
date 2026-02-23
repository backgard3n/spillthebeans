from django.db import models
from django.utils.text import slugify


class Drink(models.Model):
    LATTE = "latte"
    ESPRESSO = "espresso"
    CAPPUCCINO = "cappuccino"
    AMERICANO = "americano"
    FLAT_WHITE = "flat_white"
    MOCHA = "mocha"
    ICED = "iced"
    OTHER = "other"

    DRINK_TYPES = [
        (LATTE, "Latte"),
        (ESPRESSO, "Espresso"),
        (CAPPUCCINO, "Cappuccino"),
        (AMERICANO, "Americano"),
        (FLAT_WHITE, "Flat White"),
        (MOCHA, "Mocha"),
        (ICED, "Iced Coffee"),
        (OTHER, "Other"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    shop_name = models.CharField(max_length=120)
    drink_type = models.CharField(max_length=20, choices=DRINK_TYPES, default=OTHER)

    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Optional image upload (uses MEDIA_ROOT / MEDIA_URL)
    image = models.ImageField(upload_to="drink_images/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "shop_name")  # prevents exact duplicates

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            base = slugify(f"{self.name}-{self.shop_name}")
            slug = base
            counter = 1
            while Drink.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} @ {self.shop_name}"