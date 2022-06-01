from django.contrib import admin

# Register your models here.

from .models import Profile, Profile_profile_followers

admin.site.register(Profile)
admin.site.register(Profile_profile_followers)