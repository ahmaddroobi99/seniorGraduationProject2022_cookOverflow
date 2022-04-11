from django.urls import path
from .views import *

app_name = "Timeline"

urlpatterns = [
    path('post/create', PostCreateView.as_view(), name="post-create"),
    path('post/edit/<int:pk>', update_post, name="post-edit"),
    path('comment/create/<int:post_id>', create_comment, name="comment-create"),
]
