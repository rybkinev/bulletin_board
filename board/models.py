from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

CATEGORIES = [
    ('1', 'Танки'),
    ('2', 'Хилы'),
    ('3', 'ДД'),
    ('4', 'Торговцы'),
    ('5', 'Гилдмастеры'),
    ('6', 'Квестгиверы'),
    ('7', 'Кузнецы'),
    ('8', 'Кожевники'),
    ('9', 'Зельевары'),
    ('10', 'Мастера заклинаний')
]


class Ad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ads',
        null=True,
    )
    title = models.CharField(max_length=100, default='')
    text = RichTextUploadingField()
    category = models.CharField(
        max_length=10,
        choices=CATEGORIES,
        default='1'
    )

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Response(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='cb_response',
        null=True,
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        default=None,
        related_name='ad_responses'
    )
    accept = models.BooleanField(default=False)
    text = models.TextField(default='')
