from __future__ import unicode_literals

from django.db import models


class ChestXray(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='cxr/')
    uploaded_at = models.DateTimeField(auto_now_add=True)