from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class CountForm(forms.Form):
    count = forms.IntegerField(
        required=True,
        initial=1,
        label="Item count",
        help_text="Please input item count",
        validators=[
            MinValueValidator(1, "You can order not less than 1 item"),
            MaxValueValidator(100, "Too much, bro!"),
        ]
    )
