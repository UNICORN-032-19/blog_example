from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.CharField(max_length=50, default='anonymus', blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    create_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creators", unique=False, blank=True, null=True)
    update_uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updaters", unique=False, blank=True, null=True)

    class Meta:
        permissions = (("can_create_post", "User Can Create a new post"), )


admin.site.register(Post)
