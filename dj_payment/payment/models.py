from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Item name",
        verbose_name="Item name",
    )
    description = models.CharField(
        max_length=255,
        help_text="Item description",
        verbose_name="Item description",
    )
    price = models.FloatField(
        validators=[MinValueValidator(0, message="Price cannot be negative.")],
        help_text="Item price",
        verbose_name="Item price",
    )

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.name}"
