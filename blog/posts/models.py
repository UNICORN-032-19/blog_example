from django.db import models
from django.contrib import admin


class Post(models.Model):
    title = models.TextField()
    text = models.TextField()



admin.site.register(Post)
