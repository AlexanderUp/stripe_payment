import stripe
from django.conf import settings
from django.http import JsonResponse


def create_item_attr_dict(item, count=1):
    item_attr_dict = {
        "price_data": {
            "currency": "usd",
            "unit_amount": int(item.price * 100),
            "product_data": {
                "name": item.name,
                "description": item.description,
            },
        },
        "quantity": count,
    }
    return item_attr_dict


def create_line_items_single_purchase(item):
    return [create_item_attr_dict(item)]


def create_line_items_bunch_purchase(cart_items):
    return [
        create_item_attr_dict(cart.item, cart.count) for cart in cart_items
    ]


def create_and_call_checkout_session(line_createion_func, item_object):
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=(
                domain_url + 'success?session_id={CHECKOUT_SESSION_ID}'
            ),
            cancel_url=domain_url + "cancelled/",
            payment_method_types=["card"],
            mode="payment",
            line_items=line_createion_func(item_object)
        )
    except Exception as err:
        return JsonResponse({"error": str(err)})
    else:
        return checkout_session
