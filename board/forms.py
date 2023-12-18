from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from board.models import Bulletin


class BulletinForm(forms.ModelForm):
    title = forms.CharField(
        label='title',
        max_length=100
    )
    # text = forms.TextInput()
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Bulletin
        # fields = '__all__'
        fields = [
            'title',
            'text',
        ]
