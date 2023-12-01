import stripe
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from payment.models import TaxRate

stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(pre_save, sender=TaxRate, dispatch_uid='tax_rate_created')
def create_stripe_tax_rate(sender, instance, **kwargs):
    tax_rate = stripe.TaxRate.create(
        display_name=instance.name,
        inclusive=False,
        percentage=instance.percentage,
    )
    instance.stripe_tax_id = tax_rate['id']
