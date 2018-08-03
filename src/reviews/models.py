from django.conf import settings
from django.db import models
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

class GameReview(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=128, null=True, blank=True)
    content     = models.CharField(max_length=128, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self):
        return reverse('api-reviews:review-rud', kwargs={'pk': self.pk})

    def get_api_url(self, request=None):
        return api_reverse('api-reviews:review-rud', kwargs={'pk': self.pk}, request=request)
