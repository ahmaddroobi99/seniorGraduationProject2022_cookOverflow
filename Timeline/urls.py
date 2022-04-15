from django.urls import path
from .views import *
from Timeline.views import PostCreateView, like,favorite


app_name = "Timeline"

urlpatterns = [
    path('post/create', PostCreateView.as_view(), name="post-create"),
    path('post/edit/<int:pk>', update_post, name="post-edit"),
    path('comment/create/<int:post_id>', create_comment, name="comment-create"),
   	# path('', index, name='index'),
   	# path('newpost/', NewPost, name='newpost'),
   	# path('<uuid:post_id>', PostDetails, name='postdetails'),
   	path('<int:pk>/like', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
   	# path('tag/<slug:tag_slug>', tags, name='tags'),
]

