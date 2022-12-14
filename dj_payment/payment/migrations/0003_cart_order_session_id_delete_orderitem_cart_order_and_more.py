# Generated by Django 4.1.1 on 2022-09-19 14:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_order_orderitem_orderitem_unique_pair_order_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0, help_text='Count of item in order', validators=[django.core.validators.MinValueValidator(0, 'Item count can not be less than zero.')], verbose_name='Item count')),
                ('item', models.ForeignKey(help_text='Item Order pair', on_delete=django.db.models.deletion.CASCADE, related_name='item_order_pairs', to='payment.item', verbose_name='Item Order pair')),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='session_id',
            field=models.CharField(help_text='Session ID', max_length=32, null=True, verbose_name='Session ID'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(help_text='Order Item pair', on_delete=django.db.models.deletion.CASCADE, related_name='order_item_pairs', to='payment.order', verbose_name='Order Item pair'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('order', 'item'), name='unique_pair_order_item'),
        ),
    ]
