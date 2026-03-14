from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    list_display = ("name", "location", "owner", "is_approved")
    list_filter = ("is_approved",)

    search_fields = ("name", "location", "owner__username")

    actions = ["approve_shops"]

    def approve_shops(self, request, queryset):
        queryset.update(is_approved=True)

    approve_shops.short_description = "Approve selected shops"