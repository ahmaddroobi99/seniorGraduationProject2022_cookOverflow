from django.db import models

from Account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to="avatars/", default="avatars/guest.png")
    cover_image = models.ImageField(upload_to="avatars/", default="avatars/cover.png")
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20, blank=False, default="male")
    country = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')



@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=kwargs['instance'])
