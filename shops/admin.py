from django.contrib import admin
from .models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "location", "is_approved", "submitted_by")
    list_filter = ("is_approved",)
    search_fields = ("name", "location")