from distutils.command.upload import upload
from tkinter import CASCADE
import django
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to=('../static/ProfileImgs'))
    background_photo = models.ImageField(upload_to=('../static/ProfileImgs'))
    phoneNumber = models.IntegerField(null=True)
    country = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    dob = models.DateField()
    followers = models.ManyToManyField('self', through='Follower', symmetrical=False, related_name='related_to')

    def follow(self, user, status):
        follower, created = Follower.objects.get_or_create(
            fromUser=self,
            toUser=user,
            status=status)
        return follower

    def unFollow(self, user, status):
        Follower.objects.filter(
            fromUser=self,
            toUser=user,
            status=status).delete()
        return

    def get_relationships(self, status):
        return self.followers.filter(
            toUser__status=status,
            toUser__fromUser=self)

    def get_related_to(self, status):
        return self.related_to.filter(
            fromUser__status=status,
            fromUser__toUser=self
        )

    def get_following(self):
        return self.get_relationships(relationship_following)
    
    def get_followers(self):
        return self.get_related_to(relationship_following)

relationship_following = 1
relationship_block = 2
relationship_status = (
    (relationship_following, 'Following'),
    (relationship_block, 'Blocked'),
    )

class Follower(models.Model):
    fromUser = models.ForeignKey(Users, related_name='from_user', on_delete=models.CASCADE)
    toUser = models.ForeignKey(Users, related_name='to_user', on_delete=models.CASCADE)
    status = models.IntegerField(choices=relationship_status)

class Post(models.Model):
    postType = models.CharField(max_length=50, null=False)
    postDescription = models.TextField(null=False)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    
class Share(models.Model):
    shareName = models.CharField(max_length=50, null=False)
    shareType = models.CharField(max_length=50, null=False)
    shareDescription = models.TextField(null=False)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
