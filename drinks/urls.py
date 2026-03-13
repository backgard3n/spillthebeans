from django.urls import path
from . import views

app_name = "drinks"

urlpatterns = [
    path("", views.drink_list, name="list"),
    path("<slug:slug>/", views.drink_detail, name="detail"),
    path("shops/<slug:shop_slug>/add/", views.add_drink, name="add"),
]