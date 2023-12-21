from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from board.models import Ad, CATEGORIES, Response


class AdForm(forms.ModelForm):
    title = forms.CharField(
        label='title',
        max_length=100
    )
    category = forms.ChoiceField(choices=CATEGORIES)
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = [
            'title',
            'category',
            'text',
        ]


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = [
            'text',
        ]
