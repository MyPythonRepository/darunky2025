from django import forms
from .models import Item
from django.core.exceptions import ValidationError


class ItemForm(forms.ModelForm):
    category_name = forms.CharField(
        label="Category",
        help_text="Enter a new category or choose an existing one",
        required=True,
    )

    photo = forms.FileField(
        widget=forms.ClearableFileInput(),
        label="Photo (optional)",
        required=False,
    )

    class Meta:
        model = Item
        fields = ["name", "state", "description"]

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo and not photo.content_type.startswith("image/"):
            raise ValidationError("Only image files are allowed.")
        return photo
