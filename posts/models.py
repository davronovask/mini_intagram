from django.conf import settings
from django.db import models


class Post(models.Model):

    content = models.TextField()
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
