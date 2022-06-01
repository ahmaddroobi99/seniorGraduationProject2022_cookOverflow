from django.contrib import admin

# Register your models here.

from .models import Tag, Post, PostImage, postVideo, Comment, Follow, Likes, Stream

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(postVideo)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Likes)
admin.site.register(Stream)