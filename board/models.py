from django.db import models


class Bulletin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    # header
    # body

