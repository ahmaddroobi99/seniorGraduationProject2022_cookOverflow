import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from Friends.models import CustomNotification
from Friends.serializers import NotificationSerializer
from .forms import PostCreateForm
from .models import *


class PostCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        post = Post.objects.all().order_by('-created_at')

        context = {
            'post' : post,
        }
        return render(request, reverse_lazy('core:home'), context)

    def post(self, request, *args, **kwargs):
        post = Post.objects.all().order_by('-created_at')
        form = PostCreateForm(request.POST)
        image_files = request.FILES.getlist('image')
        video_files = request.FILES.getlist('video')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()

            for image in image_files:
                img = PostImage(image=image)
                img.save()
                new_post.image.add(img)

            new_post.save()
            
            for video in video_files:
                vid = postVideo(video=video)
                vid.save()
                new_post.video.add(vid)

            new_post.save()
        print(form.cleaned_data)
        context = {
            'post' : post,
        }
        return redirect(reverse_lazy('core:home'), context)

def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        notification = CustomNotification.objects.create(type="comment", recipient=post.user, actor=request.user, verb="commented on your post")
        channel_layer = get_channel_layer()
        channel = "comment_like_notifications_{}".format(post.user.username)
        print(json.dumps(NotificationSerializer(notification).data))
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",
                "command": "new_like_comment_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        return redirect(reverse_lazy('core:home'))
    else:
        return redirect(reverse_lazy('core:home'))
