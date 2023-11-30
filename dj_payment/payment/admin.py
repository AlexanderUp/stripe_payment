from django.contrib import admin

from payment.models import Cart, Item, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'price',
    )
    empty_value_display = '-empty-'


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'session_id',
        'description',
    )
    empty_value_display = '-empty-'


class CartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'order',
        'item',
        'count',
    )
    empty_value_display = '-empty-'


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
