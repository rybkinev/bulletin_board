from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Bulletin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='bulletin',
        null=True,
    )
    title = models.CharField(max_length=100, default='')
    # text = models.TextField(default='')
    text = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('home')
        # return reverse('/', args=[str(self.id)])
