from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=32, default='')
    phone_number = models.CharField(max_length=20, unique=True)
    is_ref = models.BooleanField(default=False)
    referrer = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='refs')
    invite_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_number

