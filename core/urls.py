from django.urls import path
from core.models.vendor import Vendor

from core.views.views import GenericView
from .auth import UserLogin, UserLogout, ping

core_urlpatterns = [
    # Auth URLS
    path("ping/", ping),
    path("login/", UserLogin.as_view()),
    path("logout/", UserLogout.as_view()),
]

api_urlpatterns = [
    path("vendors/", GenericView.as_view(model=Vendor)),
    path("vendors/<int:instance_id>/", GenericView.as_view(model=Vendor)),
]
