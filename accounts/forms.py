from django import forms


class ConfirmEmailForm(forms.Form):
    confirmation_code = forms.CharField(label='Код подтверждения', max_length=20)
