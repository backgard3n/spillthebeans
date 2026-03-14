from django.urls import path
from . import views

app_name = "accounts" 

urlpatterns = [
    path("login/", views.auth_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
]