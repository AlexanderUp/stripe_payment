from django.views.generic import DetailView

from payment.models import Item  # isort:skip


def buy_item_api(request, pk):
    pass


class ItemAPIDetailView(DetailView):
    model = Item
    template_name = "api/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_object"] = "test_key_string"
        return context
