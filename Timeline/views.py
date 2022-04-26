from dataclasses import field
import json
from pyexpat import model
import uuid

from django.template import loader

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from Friends.models import CustomNotification, Friend   
from Friends.serializers import NotificationSerializer
from Profile.models import Profile
from .forms import PostCreateForm
from .models import *


class PostCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        post = Post.objects.all()

        context = {
            'post' : post,
        }
        return render(request, reverse_lazy('core:home'), context)

    def post(self, request, *args, **kwargs):
        post = Post.objects.all()
        form = PostCreateForm(request.POST)
        image_files = request.FILES.getlist('image')
        video_files = request.FILES.getlist('video')
        tags_text = request.POST['tags']

        tags = tags_text.split("#")

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            
            for tag in tags:
                tagPost = Tag(title = tag)
                tagPost.save()
                new_post.tags.add(tagPost)

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

def deletePost(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        post.delete()
        posts = Post.objects.all()
        context = {
            'post' : posts,
        }
        return redirect(reverse_lazy('core:home'), context)
    else:
        post = Post.objects.all()

        context = {
            'post' : post,
        }
    print(post.image.all())
    return render(request, reverse_lazy('core:home'), context)


def update_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostCreateForm(instance=post)
    if request.method == "POST":
        form = PostCreateForm(request.POST, instance=post)
        image_files = request.FILES.get("images")
        print(image_files)
        video_files = request.FILES.getlist('video')
        if form.is_valid():
            print("get into if statement")
            form.save(commit=False)
            post.user = request.user

            for image in image_files:
                img = PostImage(image=image)
                img.save()
                post.image.add(img)
            
            for video in video_files:
                vid = postVideo(video=video)
                vid.save()
                post.video.add(vid)

        print(form.cleaned_data)
        return redirect(reverse_lazy('core:home'), {"post": post})
    else:
        form = PostCreateForm(instance=post)
    
    context = {
        "pk":post.id,
        "content":post.body,
        "imageFiles":post.image.all(),
    }
    print(post.image.all())
    return render(request, "post_edit.html", context)

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


def tags(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tag.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))





@login_required
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return HttpResponseRedirect(reverse('core:home', args=[post_id]))

@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('core:home', args=[post_id]))


