from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
   path('',views.index ,name= "timeline"),
   path('timeline/',views.index ,name= "timeline"),
   path('profile/',views.profile ,name= "profile"),
]
