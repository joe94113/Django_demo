from django import forms
from django.forms import PasswordInput


class Login_form(forms.Form):
    username = forms.CharField(required=True)  # 使用者一定要輸入
    password = forms.CharField(required=True, widget=PasswordInput)
