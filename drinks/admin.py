from django.contrib import admin
from .models import Shop, Drink

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("drink_type", "shop")
    search_fields = ("name", "shop__name")
    list_display = ("name", "shop", "drink_type", "price")