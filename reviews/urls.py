from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("drink/add/<int:drink_id>/", views.add_drink_review, name="add_drink"),
    path("shop/<slug:shop_slug>/add/", views.add_shop_review, name="add_shop"),
]