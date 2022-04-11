from distutils.command.upload import upload
from typing import OrderedDict
from django.db import models

from Account.models import User
from django.utils.timezone import now


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    image = models.ManyToManyField('PostImage', blank=True)
    video = models.ManyToManyField('postVideo', blank=True)
    created_at = models.DateTimeField(default=now)
    class Meta:
        ordering = ("-created_at",)

class PostImage(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=False)

class postVideo(models.Model):
    video = models.FileField(upload_to="videos/", blank=True, null=False)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
