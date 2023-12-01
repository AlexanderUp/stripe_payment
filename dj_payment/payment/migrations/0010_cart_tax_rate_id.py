# Generated by Django 4.2.7 on 2023-12-01 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payment', '0009_alter_item_price_alter_taxrate_stripe_tax_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax_rate_id',
            field=models.ForeignKey(
                blank=True,
                help_text='tax rate id',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cart_items',
                to='payment.taxrate',
                verbose_name='tax_rate_id',
            ),
        ),
    ]
