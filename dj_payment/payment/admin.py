from django.contrib import admin

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "price",
    )
    empty_value_display = "-empty-"


admin.site.register(Item, ItemAdmin)
