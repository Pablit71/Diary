from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(verbose_name='chat ID', unique=True)
    username = models.CharField(verbose_name='Username', max_length=255, blank=True, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    verification_code = models.CharField(max_length=100, null=True, blank=True, default=None)
