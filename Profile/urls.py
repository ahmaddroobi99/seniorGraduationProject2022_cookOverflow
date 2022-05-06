from django.urls import path
from .views import *
app_name = "profile"

urlpatterns = [
    path('edit-profile', ProfileEditView.as_view(), name="edit-profile"),
    path('profile/<int:pk>', ProfileView.as_view(), name="user-timeline"),

   	path('like/<int:post_id>', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('search/', UserSearch.as_view(), name='profile-search'),
]
