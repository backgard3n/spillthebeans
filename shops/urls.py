from django.urls import path
from . import views

app_name = "shops"

urlpatterns = [
    path("", views.shop_list, name="shop_list"),
    path("add/", views.add_shop, name="add_shop"),
    path("<slug:slug>/", views.shop_detail, name="shop_detail"),
]