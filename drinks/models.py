from django.db import models
from django.utils.text import slugify
from shops.models import Shop


class Drink(models.Model):
    # Drink type choices
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

    slug = models.SlugField(max_length=160, unique=True, blank=True)

    # 🔥 IMPORTANT CHANGE: ForeignKey to shops.Shop
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="drinks"
    )

    drink_type = models.CharField(
        max_length=20,
        choices=DRINK_TYPES,
        default=OTHER
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="drink_images/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "shop")  # prevents duplicate drink names per shop

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.name}-{self.shop.name}")
            slug = base
            counter = 1
            while Drink.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} @ {self.shop.name}"