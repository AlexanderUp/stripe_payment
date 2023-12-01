# Generated by Django 4.2.7 on 2023-12-01 14:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payment', '0011_rename_tax_rate_id_cart_tax_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Discount name',
                        max_length=255,
                        verbose_name='Discount',
                    ),
                ),
                (
                    'percentage',
                    models.DecimalField(
                        decimal_places=4,
                        help_text='Discount percentage',
                        max_digits=6,
                        verbose_name='percentage',
                    ),
                ),
                (
                    'stripe_discount_id',
                    models.CharField(
                        blank=True,
                        help_text='Stripe discount ID',
                        max_length=64,
                        null=True,
                        verbose_name='stipe_discount_id',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Tax Rate',
                'verbose_name_plural': 'Tax Rates',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='discount',
            field=models.ForeignKey(
                blank=True,
                help_text='discount id',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cart_items',
                to='payment.discount',
                verbose_name='discount_id',
            ),
        ),
    ]
