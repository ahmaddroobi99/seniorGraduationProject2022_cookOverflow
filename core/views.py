from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q

# from Friends.models import Friend
from Timeline.models import Post


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('Account:Register'))

    # friends_one = Friend.objects.filter(friend=request.user).filter(status='friend')
    # friends_two = Friend.objects.filter(user=request.user).filter(status='friend')
    # friends_list_one = list(friends_one.values_list('user_id', flat=True))
    # friends_list_two = list(friends_two.values_list('friend_id', flat=True))
    # friends_list_id = friends_list_one + friends_list_two + [request.user.id]
    # friends = friends_one.union(friends_two)
    posts = Post.objects.all()
    # return render(request, 'home.html', {'posts': posts, 'friends': friends})
    
    return render(request, 'home.html', {'posts': posts})