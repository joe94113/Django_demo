from django import forms


class Django_form(forms.Form):
    content = forms.CharField(required=True)  # 使用者一定要輸入
    email = forms.EmailField()