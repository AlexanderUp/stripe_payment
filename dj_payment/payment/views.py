import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import (DetailView, ListView, RedirectView,
                                  TemplateView)

from .models import Item


class BuyView(RedirectView):

    def get_object(self):
        return Item.objects.get(pk=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs.get("pk"))
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(item.price * 100),
                            "product_data": {
                                "name": item.name,
                                "description": item.description,
                            },
                        },
                        "quantity": 1,
                    }
                ]
            )
        except Exception as err:
            return JsonResponse({"error": str(err)})
        else:
            return redirect(checkout_session.url, code=303)


class ItemDetailView(DetailView):
    model = Item


class IndexListView(ListView):
    model = Item
    template_name = "payment/index.html"


class SuccessTemplateView(TemplateView):
    template_name = "payment/success_payment.html"


class CancelledTemplateView(TemplateView):
    template_name = "payment/cancelled_payment.html"