from django.urls import path

from .views import ItemAPIDetailView, buy_item_api

app_name = "api"

urlpatterns = [
    path("buy/<int:pk>/", buy_item_api, name="buy_item_api"),  # type:ignore
    path(
        "item/<int:pk>/", ItemAPIDetailView.as_view(), name="item_detail_api_view"  # type:ignore
    ),
]
