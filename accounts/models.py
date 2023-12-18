from django.db import models


class EmailVerify(models.Model):
    email = models.EmailField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    key = models.IntegerField(default=0)
    sent = models.DateTimeField(auto_now_add=True)
