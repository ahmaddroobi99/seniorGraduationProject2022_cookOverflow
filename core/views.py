from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q

# from Friends.models import Friend
from Timeline.models import Post
from Profile.models import Profile, Profile_profile_followers


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('Account:Register'))

    # friends_one = Friend.objects.filter(friend=request.user).filter(status='friend')
    # friends_two = Friend.objects.filter(user=request.user).filter(status='friend')
    # friends_list_one = list(friends_one.values_list('user_id', flat=True))
    # friends_list_two = list(friends_two.values_list('friend_id', flat=True))
    # friends_list_id = friends_list_one + friends_list_two + [request.user.id]
    # friends = friends_one.union(friends_two)
    profile = Profile.objects.get(user=request.user)
    followers = Profile_profile_followers.objects.filter(user_id = request.user.id)
    followersList = []
    for follower in followers:
        followersList.append(follower.profile_id)
    followersList.append(request.user.id)
    print()
    print()
    print()
    print(followersList)
    print()
    print()
    print()
    post = Post.objects.filter(user__id__in = followersList)
    context = {
            'posts' : post,
        }
    # return render(request, 'home.html', {'posts': posts, 'friends': friends})
    
    return render(request, 'home.html', context)