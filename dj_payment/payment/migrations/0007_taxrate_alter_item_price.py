# Generated by Django 4.2.7 on 2023-12-01 11:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payment', '0006_alter_cart_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxRate',
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
                        help_text='Tax Rate name', max_length=255, verbose_name='TaxRate'
                    ),
                ),
                (
                    'percentage',
                    models.DecimalField(
                        decimal_places=4,
                        help_text='Tax Rate percentage',
                        max_digits=6,
                        verbose_name='percentage',
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(
                decimal_places=6,
                help_text='Item price',
                max_digits=12,
                validators=[
                    django.core.validators.MinValueValidator(
                        0, message='Price cannot be negative.'
                    )
                ],
                verbose_name='Item price',
            ),
        ),
    ]