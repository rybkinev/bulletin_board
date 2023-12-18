from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from board.models import Bulletin, CATEGORIES


class BulletinForm(forms.ModelForm):
    title = forms.CharField(
        label='title',
        max_length=100
    )
    category = forms.ChoiceField(choices=CATEGORIES)
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Bulletin
        fields = [
            'title',
            'category',
            'text',
        ]
