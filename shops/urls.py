from django.urls import path
from . import views

app_name = "shops"

urlpatterns = [
    path("", views.shop_list, name="list"),
    path("add/", views.add_shop, name="add"),
    path("<slug:slug>/", views.shop_detail, name="detail"),
    path("<slug:slug>/edit/", views.edit_shop, name="edit"),
]
