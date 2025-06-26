from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ["user_type"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["name"].initial = user.name
            self.fields["email"].initial = user.email
            self.fields["avatar"].initial = user.avatar

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        user.name = self.cleaned_data["name"]
        user.email = self.cleaned_data["email"]

        avatar = self.cleaned_data.get("avatar")

        if avatar is False:
            if user.avatar:
                user.avatar.delete(save=False)
            user.avatar = None
        elif avatar:
            user.avatar = avatar

        if commit:
            user.save()
            profile.save()
        return profile
