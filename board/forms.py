from ckeditor.fields import RichTextField
from django import forms

from board.models import Bulletin


class BulletinForm(forms.ModelForm):
    title = forms.CharField(
        label='title',
        max_length=100
    )
    # text = forms.TextInput()
    text = RichTextField(config_name='multi_image_config')

    class Meta:
        model = Bulletin
        # fields = '__all__'
        fields = [
            'title',
            'text',
        ]
