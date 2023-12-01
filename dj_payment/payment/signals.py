import stripe
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from payment.models import Discount, TaxRate

stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(post_save, sender=TaxRate, dispatch_uid='tax_rate_created')
def create_stripe_tax_rate(sender, instance, created, **kwargs):
    if created:
        tax_rate = stripe.TaxRate.create(
            display_name=instance.name,
            inclusive=False,
            percentage=instance.percentage,
        )
        instance.stripe_tax_id = tax_rate['id']
        instance.save()


@receiver(post_save, sender=Discount, dispatch_uid='discount_created')
def create_stripe_discount(sender, instance, created, **kwargs):
    if created:
        discount = stripe.Coupon.create(
            percent_off=instance.percentage,
            duration='forever',
        )
        instance.stripe_discount_id = discount['id']
        instance.save()
