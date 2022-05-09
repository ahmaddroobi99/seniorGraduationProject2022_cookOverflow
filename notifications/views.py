from django.http import JsonResponse
from django.shortcuts import render
from Profile.models import Profile_profile_followers

# from Friends.models import CustomNotification


def mark_like_comment_notifications_as_read(request):
    CustomNotification.objects.filter(recipient=request.user, type="comment").update(unread=False)
    return JsonResponse({
        'status': True,
        'message': "Marked all notifications as read"
    })


from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification


# Create your views here.

def ShowNOtifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    template = loader.get_template('notifications.html')

    followers = Profile_profile_followers.objects.filter(user_id = request.user.id)


    followersList = []
    for follower in followers:
        followersList.append(follower.profile_id)
    
    number_of_notification = Notification.objects.filter(is_seen = False).count()

    context = {
        'notifications': notifications,
        'numberOfNotification':number_of_notification, 
    }

    return HttpResponse(template.render(context, request))


def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notifications')


def CountNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

    return {'count_notifications': count_notifications}



