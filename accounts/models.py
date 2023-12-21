from django.contrib.auth.models import User
from django.db import models

from board.models import CATEGORIES


class EmailVerify(models.Model):
    email = models.EmailField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    key = models.IntegerField(default=0)
    sent = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORIES,
        default='1'
    )
