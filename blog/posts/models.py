from django.db import models
from django.contrib import admin


class Post(models.Model):
    author = models.CharField(max_length=50, default='anonymus', blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


admin.site.register(Post)
