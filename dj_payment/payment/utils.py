import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_item_attr_dict(item, stripe_tax_id='txr_1OIWi2I74MU8cGTf68xStRKW', count=1):
    return {
        'price_data': {
            'currency': 'usd',
            'unit_amount': int(item.price * 100),
            'product_data': {
                'name': item.name,
                'description': item.description,
            },
        },
        'quantity': count,
        'tax_rates': [stripe_tax_id],
    }


def create_line_items_single_purchase(item):
    return [create_item_attr_dict(item)]


def create_line_items_bunch_purchase(cart_items):
    return [
        create_item_attr_dict(
            cart.item,
            cart.tax_rate.stripe_tax_id,
            cart.count,
        )
        for cart in cart_items
    ]


def create_and_call_checkout_session(line_creation_func, item_object):
    domain_url = settings.DOMAIN_URL

    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=(domain_url + 'success'),
            cancel_url=(domain_url + 'cancelled'),
            payment_method_types=['card'],
            mode='payment',
            line_items=line_creation_func(item_object),
        )
    except Exception as err:
        return JsonResponse({'error': str(err)})
    return checkout_session
