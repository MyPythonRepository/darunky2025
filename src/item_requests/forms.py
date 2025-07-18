from django import forms
from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["name", "phone", "delivery_address"]
        widgets = {
            "delivery_address": forms.Textarea(attrs={"rows": 3}),
        }
