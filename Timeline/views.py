from dataclasses import field
import json
from pyexpat import model
import uuid

from django.template import loader

from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q


# from Friends.models import CustomNotification, Friend   
# from Friends.serializers import NotificationSerializer
from Profile.models import Profile, Profile_profile_followers
from .forms import PostCreateForm
from .models import *


class PostCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        followers = profile.followers.all()
        print()
        print()
        print()
        print(followers)
        print()
        print()
        print()
        followersList = []
        for follower in followers:
            followersList.append(follower.profile_id)
        
        number_of_notification = Notification.objects.filter(is_seen = False).count()
    
        post = Post.objects.filter(user = request.user or user in followers)

        context = {
            'post' : post,
            'numberOfNotification':number_of_notification, 

        }
        return render(request, reverse_lazy('core:home'), context)

    def post(self, request, *args, **kwargs):
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
        return redirect(reverse_lazy('core:home'))

def deletePost(request, pk):
    post = get_object_or_404(Post, id=pk)
    tag = get_object_or_404(Tag, id=pk)

    if request.method == "POST":

        for tag in post.tags.all():
            tag.delete()

        for image in post.image.all():
            image.delete()

        for video in post.video.all():
            video.delete()
        
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


def preview_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    followers = Profile_profile_followers.objects.filter(user_id = request.user.id)
    followersList = []
    for follower in followers:
        followersList.append(follower.profile_id)
    
    number_of_notification = Notification.objects.filter(is_seen = False).count()

    context = {
        'post':post,
        'numberOfNotification':number_of_notification, 
    }
    return render(request, "post_edit.html", context)

def tags_preview(request, title="`"):
    tags = Tag.objects.all().values_list('title', flat=True).distinct()[:10]
    number_of_notification = Notification.objects.filter(is_seen = False).count()

    if title != "`":    
        posts = Post.objects.filter(tags__title = title)
    else:
        posts = None
    context = {
        "posts": posts,
        "tags": tags,
        'numberOfNotification':number_of_notification, 
    }

    return render(request, "tags.html", context)


def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        # notification = CustomNotification.objects.create(type="comment", recipient=post.user, actor=request.user, verb="commented on your post")
        # channel_layer = get_channel_layer()
        # channel = "comment_like_notifications_{}".format(post.user.username)
        # print(json.dumps(NotificationSerializer(notification).data))
        # async_to_sync(channel_layer.group_send)(
        #     channel, {
        #         "type": "notify",
        #         "command": "new_like_comment_notification",
        #         "notification": json.dumps(NotificationSerializer(notification).data)
        #     }
        # )

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

        #return HttpResponseRedirect(reverse('core:home', args=[post_id]))
    
    return redirect(reverse_lazy('core:home'))

# @login_required
def findFriends(request):
    
    template = loader.get_template('find-friends.html')  
    usersList = []
    number_of_notification = Notification.objects.filter(is_seen = False).count()
    followers = []
    followersList = []

    if request.method == "POST":     
        friendToSearch = request.POST.get("friendToSearch")

        users = Profile.objects.filter(user__username__icontains = friendToSearch)

        for user in users:
            if user.user.id != request.user.id:
                usersList.append(user)
        followers = Profile_profile_followers.objects.filter(user_id = request.user.id)
        for follower in followers:
            followersList.append(follower.profile_id)
        

        print()
        print()
        print(followersList)
        print()
        print()

    context = {
        'usersList': usersList,
        'numberOfNotification':number_of_notification, 
        'followers': followersList,
    }
    return HttpResponse(template.render(context, request))

# def follow(request, pk):
#     user = request.user
#     is_follower = False

#     followers = Profile_profile_followers.objects.filter(user_id = request.user.id)
#     followersList = []
#     for follower in followers:
#         followersList.append(follower.profile_id)
    
#     if pk in followersList:


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


