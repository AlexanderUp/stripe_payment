from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from payment.forms import CountForm
from payment.models import Cart, Item, Order, TaxRate
from payment.utils import (
    create_and_call_checkout_session,
    create_line_items_bunch_purchase,
    create_line_items_single_purchase,
)


class BuyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(pk=self.kwargs.get('pk'))
        stripe_session = create_and_call_checkout_session(
            create_line_items_single_purchase,
            item,
        )
        return JsonResponse({'session_id': stripe_session.id})


class CartBuyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = (
            Cart.objects.filter(order__session_id=request.session.session_key)
            .select_related('item')
            .all()
        )
        if not cart_items:
            context = {
                'error_message': 'Empty cart is not allowed to proceed with payment.',
            }
            return render(request, 'payment/error_template.html', context=context)
        session = create_and_call_checkout_session(
            create_line_items_bunch_purchase,
            cart_items,
        )
        return redirect(session.url, code=HTTPStatus.SEE_OTHER)


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_pub_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class IndexListView(ListView):
    model = Item
    template_name = 'payment/index.html'


class SuccessTemplateView(TemplateView):
    template_name = 'payment/success_payment.html'

    def get(self, request, *args, **kwargs):
        Cart.objects.filter(order__session_id=request.session.session_key).delete()
        return super().get(request, *args, **kwargs)


class CancelledTemplateView(TemplateView):
    template_name = 'payment/cancelled_payment.html'


class CartListView(ListView):
    template_name = 'payment/cart.html'

    def get_queryset(self):
        session_id = self.request.session.session_key
        if not session_id:
            return HttpResponse('Problem with <session_key>!')
        return Cart.objects.select_related('item', 'order').filter(
            order__session_id=session_id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        carts = Cart.objects.select_related('item', 'order').filter(
            order__session_id=self.request.session.session_key,
        )
        total_price = sum((cart.item.price * cart.count) for cart in carts)
        total_taxes = sum(
            (cart.item.price * cart.tax_rate.percentage / 100) for cart in carts
        )
        grand_total = sum(
            (cart.item.price * cart.count * (1 + cart.tax_rate.percentage / 100))
            for cart in carts
        )
        context['total_price'] = total_price
        context['total_taxes'] = total_taxes
        context['grand_total'] = grand_total
        return context


class ItemDeletedTemplateView(TemplateView):
    template_name = 'payment/item_deleted.html'


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        order, _ = Order.objects.get_or_create(
            session_id=request.session.session_key,
        )
        count = 1
        default_tax_rate = TaxRate.objects.last()
        cart, is_cart_created = Cart.objects.get_or_create(
            order=order,
            item=item,
            count=count,
            tax_rate=default_tax_rate,
        )
        if not is_cart_created:
            return HttpResponse(f'{cart} has been already created!')
        return redirect(reverse('payment:index'))


class DeleteFromCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        cart = Cart.objects.get(
            item__pk=self.kwargs.get('pk'),
            order__session_id=session_key,
        )
        cart.delete()
        return redirect(reverse_lazy('payment:item_deleted_from_cart'))


class SetItemCountForm(FormView):
    form_class = CountForm
    template_name = 'payment/set_item.html'
    success_url = reverse_lazy('payment:cart')

    def form_valid(self, form):
        cart = get_object_or_404(
            Cart,
            order__session_id=self.request.session.session_key,
            item__id=self.kwargs.get('pk'),
        )
        cart.count = form.cleaned_data.get('count')
        cart.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_initial(self):
        cart = get_object_or_404(
            Cart,
            order__session_id=self.request.session.session_key,
            item__id=self.kwargs.get('pk'),
        )
        return {'count': cart.count}
