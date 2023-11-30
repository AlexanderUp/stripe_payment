from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    session_id = models.CharField(
        max_length=32,
        verbose_name='Session ID',
        help_text='Session ID',
        unique=True,
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Order description',
        help_text='Order description',
        null=True,
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('-id',)

    def __str__(self):
        return f'Order({self.session_id})'


class Item(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='Item name',
        verbose_name='Item name',
    )
    description = models.CharField(
        max_length=255,
        help_text='Item description',
        verbose_name='Item description',
    )
    price = models.FloatField(
        validators=[MinValueValidator(0, message='Price cannot be negative.')],
        help_text='Item price',
        verbose_name='Item price',
    )

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ('-id',)

    def __str__(self):
        return f'Item({self.name})'


class Cart(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_cart_pairs',
        verbose_name='Order Cart pair',
        help_text='Order Cart pair',
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='item_cart_pairs',
        verbose_name='Item Cart pair',
        help_text='Item Cart pair',
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name='Item count',
        help_text='Count of item in order',
        validators=[MinValueValidator(0, 'Item count can not be less than zero.')],
    )

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'item'], name='unique_pair_order_item'
            ),
        ]

    def __str__(self):
        return f'Cart({self.order})-{self.item}-Count({self.count})'
