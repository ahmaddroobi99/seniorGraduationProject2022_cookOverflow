from django.db import models

from Account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications.models import Notification



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


class Profile_profile_followers(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.profile.user
        following = follow.user
        notify = Notification(sender=sender, user=following, notification_type=3)
        notify.save()

    # def user_unfollow(sender, instance, *args, **kwargs):
    #     follow = instance
    #     sender = follow.profile.user
    #     following = follow.user

    #     notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
    #     notify.delete()

    class Meta:
        managed = False
        db_table = 'Profile_profile_followers'
        unique_together = (('profile_id', 'user_id'),)


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.create(user=kwargs['instance'])
