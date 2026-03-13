from django.contrib import admin
from .models import DrinkReview, ShopReview

@admin.register(DrinkReview)
class DrinkReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "drink", "created_at")
    search_fields = ("user__username", "drink__name")
    list_filter = ("created_at",)

@admin.register(ShopReview)
class ShopReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "shop", "overall_score", "created_at")
    search_fields = ("user__username", "shop__name")
    list_filter = ("created_at", "overall_score")