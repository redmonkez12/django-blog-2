from django import forms
from django.contrib.auth.models import User

from .models import Comment


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passswords don't match")
        return cd["password2"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]