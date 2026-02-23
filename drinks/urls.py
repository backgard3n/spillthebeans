from django.urls import path
from . import views

app_name = "drinks"

urlpatterns = [
    path("", views.drink_list, name="list"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("<slug:slug>/", views.drink_detail, name="detail"),
]