from django import forms


class AuthForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput)
