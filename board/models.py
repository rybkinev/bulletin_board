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
    category = models.CharField(
        max_length=10,
        choices=CATEGORIES,
        default='1'
    )

    @property
    def category_display(self):
        return self.get_category_display()

    def get_absolute_url(self):
        return reverse('home')
        # return reverse('/', args=[str(self.id)])
