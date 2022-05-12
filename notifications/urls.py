from django.urls import path
from .views import *

app_name = "notifications"

urlpatterns = [
	path('', ShowNOtifications, name='show-notifications'),
   	path('delete/<int:id>', DeleteNotification, name='delete-notification'),
    path('mark-like-comment-notifications-as-read', mark_like_comment_notifications_as_read, name="mark-like-comment-notifications-as-read"),
]
