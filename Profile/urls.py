from django.urls import path
from .views import *
app_name = "profile"

urlpatterns = [
    path('edit-profile', ProfileEditView.as_view(), name="edit-profile"),
    path('profile/<int:pk>', TimelineView.as_view(), name="user-timeline"),
   	path('like/<int:post_id>', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
]
