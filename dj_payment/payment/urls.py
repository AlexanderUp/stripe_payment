from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path("success/", views.SuccessTemplateView.as_view(), name="success"),
    path(
        "cancelled/", views.CancelledTemplateView.as_view(), name="cancelled"
    ),
    path("buy/<int:pk>/", views.BuyView.as_view(), name="buy"),
    path("item/<int:pk>/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("item/<int:pk>/", views.ItemDetailView.as_view(), name="item"),
    path(
        "cart/item/<int:pk>/delete_from_cart/",
        views.delete_from_cart,
        name="delete_from_cart"
    ),
    # path(
    #     "cart/item/<int:pk>/set_item_count/",
    #     views.set_item_count,
    #     name="set_item_count"
    # ),
    path(
        "cart/item/<int:pk>/set_item_count/",
        views.SetItemCountForm.as_view(),
        name="set_item_count"
    ),
    path(
        "cart/deleted_from_cart_success",
        views.ItemDeletedTemplateView.as_view(),
        name="item_deleted_from_cart"
    ),
    path(
        "cart/proceed_with_payment/",
        views.CartBuyView.as_view(),
        name="proceed_with_payment"
    ),
    path("cart/", views.CartListView.as_view(), name="cart"),
    path("", views.IndexListView.as_view(), name="index"),
]
