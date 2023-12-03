from django.urls import path
from .auth import UserLogin, UserLogout, ping

core_urlpatterns = [
    # Auth URLS
    path("ping/", ping),
    path("login/", UserLogin.as_view()),
    path("logout/", UserLogout.as_view()),
]
