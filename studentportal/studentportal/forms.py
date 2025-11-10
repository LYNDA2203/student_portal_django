from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from mentor.models import UserProfile

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150,label="Username",validators=[RegexValidator(r'^[\w.@+\-\s]+$', "Enter a valid username.")],)
    email = forms.EmailField(required=True, label="Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password",help_text="Enter a strong password.")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password",help_text="Enter a strong password.")
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, label="Role")
    mentor_username = forms.CharField(required=False, help_text="(Optional) Enter your mentor’s username")
    
    
    
    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don’t match!")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Save role in UserProfile
            role = self.cleaned_data["role"]
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
        return user

