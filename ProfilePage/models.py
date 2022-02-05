from distutils.command.upload import upload
from enum import unique
from django.utils import timezone
from unicodedata import decimal
import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.forms import EmailField

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        
        if other_fields.get('is_active') is not True:
            raise ValueError("Superuser must be assigned to is_active=True")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        
        if not email:
            raise ValueError("You must provide an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class Cooker(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True)
    start_date = models.DateField(default=timezone.now)
    profile_photo = models.ImageField(upload_to=('../static/ProfileImgs'))
    background_photo = models.ImageField(upload_to=('../static/ProfileImgs'))
    bio = models.TextField(null=True)
    phoneNumber = models.IntegerField(null=True)
    country = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    rating = models.FloatField(null=False, default=0)
    followers = models.ManyToManyField('self', through='Follower', symmetrical=False, related_name='related_to')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS  = ['user_name']

    def __str__(self):
        return self.user_name

    # create / Insert / add - POST
    # Retrieve / Fetch - GET
    # Update / Edit - PUT
    # Delete / Remove - DELETE

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
    fromUser = models.ForeignKey(Cooker, related_name='from_user', on_delete=models.CASCADE)
    toUser = models.ForeignKey(Cooker, related_name='to_user', on_delete=models.CASCADE)
    status = models.IntegerField(choices=relationship_status)

class Post(models.Model):
    postType = models.CharField(max_length=50, null=False)
    postDescription = models.TextField(null=False)
    userID = models.ForeignKey(Cooker, on_delete=models.CASCADE)
    
class Share(models.Model):
    shareName = models.CharField(max_length=50, null=False)
    shareType = models.CharField(max_length=50, null=False)
    shareDescription = models.TextField(null=False)
    userID = models.ForeignKey(Cooker, on_delete=models.CASCADE)
