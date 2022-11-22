from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (DetailView, ListView, RedirectView,
                                  TemplateView)
from django.views.generic.edit import FormView

from .forms import CountForm
from .models import Cart, Item, Order
from .utils import (create_and_call_checkout_session,
                    create_line_items_bunch_purchase,
                    create_line_items_single_purchase)


class BuyView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs.get("pk"))
        session = create_and_call_checkout_session(
            create_line_items_single_purchase, item
        )
        return redirect(session.url, code=303)


class CartBuyView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(
            order__session_id=request.session.session_key
        ).select_related("item").all()
        if not cart_items:
            context = {
                "error_message": "Empty cart is not allowed to proceed with payment."
            }
            return render(
                request, "payment/error_template.html", context=context
            )
        session = create_and_call_checkout_session(
            create_line_items_bunch_purchase, cart_items
        )
        return redirect(session.url, code=303)


class ItemDetailView(DetailView):
    model = Item


class IndexListView(ListView):
    model = Item
    template_name = "payment/index.html"


class SuccessTemplateView(TemplateView):
    template_name = "payment/success_payment.html"

    def get(self, request, *args, **kwargs):
        Cart.objects.filter(
            order__session_id=request.session.session_key
        ).delete()
        return super().get(request, *args, **kwargs)


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
        context = super().get_context_data()
        carts = Cart.objects.select_related("item", "order").filter(
            order__session_id=self.request.session.session_key
        )
        total_price = sum(
            (cart.item.price * cart.count) for cart in carts
        )
        context["total_price"] = total_price
        return context


class ItemDeletedTemplateView(TemplateView):
    template_name = "payment/item_deleted.html"


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user.is_anonymous:
        context = {
            "error_message": "Anonymous user is not allowed!",
        }
        return render(
            request, "payment/error_template.html", context=context
        )
    order, is_order_created = Order.objects.get_or_create(
        session_id=request.session.session_key
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


class SetItemCountForm(FormView):
    form_class = CountForm
    template_name = "payment/set_item.html"
    success_url = reverse_lazy("payment:cart")

    def form_valid(self, form):
        cart = get_object_or_404(
            Cart,
            order__session_id=self.request.session.session_key,
            item__id=self.kwargs.get("pk")
        )
        cart.count = form.cleaned_data.get("count")
        cart.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(pk=self.kwargs.get("pk"))
        return context

    def get_initial(self):
        cart = get_object_or_404(
            Cart,
            order__session_id=self.request.session.session_key,
            item__id=self.kwargs.get("pk")
        )
        return {"count": cart.count}
