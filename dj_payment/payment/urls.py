from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path("success/", views.SuccessTemplateView.as_view(), name="success"),
    path(
        "cancelled/", views.CancelledTemplateView.as_view(), name="cancelled"
    ),
    path("buy/<int:pk>/", views.BuyView.as_view(), name="buy"),
    path("item/<int:pk>/", views.ItemDetailView.as_view(), name="item"),
    path("", views.IndexListView.as_view(), name="index"),
]
