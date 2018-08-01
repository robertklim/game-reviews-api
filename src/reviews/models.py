from django.conf import settings
from django.db import models

class GameReview(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=128, null=True, blank=True)
    content     = models.CharField(max_length=128, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title