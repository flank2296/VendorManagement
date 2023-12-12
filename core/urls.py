from django.urls import path

from core.auth import UserLogin, UserLogout, ping
from core.models.historical_performance import HistoricalPerformance
from core.models.purchase_order import PurchaseOrder
from core.models.vendor import Vendor
from core.views.views import GenericView

core_urlpatterns = [
    # Auth URLS
    path("ping/", ping),
    path("login/", UserLogin.as_view()),
    path("logout/", UserLogout.as_view()),
]

GENERIC_API_URL_MODEL_MAPPER = {"vendors": Vendor, "purchase_orders": PurchaseOrder}

api_urlpatterns = []
for url, model in GENERIC_API_URL_MODEL_MAPPER.items():
    api_urlpatterns.append(path(f"{url}/", GenericView.as_view(model=model))),
    api_urlpatterns.append(
        path(f"{url}/<int:instance_id>/", GenericView.as_view(model=model))
    ),

# Vendor Performance URLs
api_urlpatterns += [
    path(
        f"vendors/<int:instance_id>/performance/",
        GenericView.as_view(model=HistoricalPerformance),
    ),
]
