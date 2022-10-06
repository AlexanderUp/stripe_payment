from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (DetailView, ListView, RedirectView,
                                  TemplateView)

from .forms import CountForm
from .models import Cart, Item, Order
from .utils import (create_and_call_checkout_session,
                    create_line_items_bunch_purchase,
                    create_line_items_single_purchase)


class BuyView(RedirectView):

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs.get("pk"))
        url = create_and_call_checkout_session(
            create_line_items_single_purchase, item
        )
        return redirect(url, code=303)


class CartBuyView(RedirectView):

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(
            order__session_id=request.session.session_key
        ).select_related("item").all()
        url = create_and_call_checkout_session(
            create_line_items_bunch_purchase, cart_items
        )
        return redirect(url, code=303)


class ItemDetailView(DetailView):
    model = Item


class IndexListView(ListView):
    model = Item
    template_name = "payment/index.html"


class SuccessTemplateView(TemplateView):
    template_name = "payment/success_payment.html"


class CancelledTemplateView(TemplateView):
    template_name = "payment/cancelled_payment.html"


class CartListView(ListView):
    template_name = "payment/cart.html"

    def get_queryset(self):
        session_id = self.request.session.session_key
        if not session_id:
            return HttpResponse("Problem with <session_key>!")
        return (Cart.objects
                    .select_related("item", "order")
                    .filter(order__session_id=session_id))

    def get_context_data(self, **kwargs):
        content = super().get_context_data()
        carts = Cart.objects.select_related("item", "order").filter(
            order__session_id=self.request.session.session_key
        )
        total_price = sum(
            (cart.item.price * cart.count) for cart in carts
        )
        content["total_price"] = total_price
        return content


class ItemDeletedTemplateView(TemplateView):
    template_name = "payment/item_deleted.html"


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user.is_anonymous:
        return HttpResponse("Anonymous user is not allowed!")
    session_id = request.session.session_key
    order, is_order_created = Order.objects.get_or_create(
        session_id=session_id
    )
    count = 1
    cart, is_cart_created = Cart.objects.get_or_create(
        order=order, item=item, count=count
    )
    if not is_cart_created:
        return HttpResponse(f"{cart} has been already created!")
    return redirect(reverse("payment:index"))


def delete_from_cart(request, pk):
    session_key = request.session.session_key
    cart = Cart.objects.get(item__pk=pk, order__session_id=session_key)
    cart.delete()
    return redirect(reverse_lazy("payment:item_deleted_from_cart"))


def set_item_count(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart = get_object_or_404(
        Cart,
        order__session_id=request.session.session_key,
        item=item
    )
    form = CountForm(
        request.POST or None,
        initial={
            "count": cart.count
        }
    )
    if form.is_valid():
        cart.count = form.cleaned_data.get("count")
        cart.save()
        return redirect(reverse("payment:cart"))
    context = {
        "item": item,
        "form": form
    }
    return render(request, "payment/set_item.html", context)
