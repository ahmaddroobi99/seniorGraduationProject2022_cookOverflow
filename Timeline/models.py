from distutils.command.upload import upload
from django.db import models

from Accounts.models import User
from django.utils.timezone import now


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(default=now)

# class PostImage(models.Model):
#     post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
#     image = models.ImageField()

# class postVideo(models.Model):
#     post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
#     video = models.FileField(upload_to="videos/", null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
