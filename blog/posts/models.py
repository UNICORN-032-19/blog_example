from django.db import models
from django.contrib import admin


class Post(models.Model):
    author = models.TextField(default='anonymus')
    title = models.TextField()
    text = models.TextField()


admin.site.register(Post)
