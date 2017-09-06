from django.contrib.auth.models import User
from django import forms

class UserForm(forms.Form):
    Username=forms.CharField(max_length=30)
    Password =forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['Username', ' Password']