from django import forms
from django.contrib.auth.forms import UserCreationForm
from mentor.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")