from django.contrib import admin

from django.urls import path, include
from .models import Message

app_name = "communications"

admin.site.register(Message)