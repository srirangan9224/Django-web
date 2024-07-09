from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,related_name="person")
    dp = models.URLField(default=None)
    following = models.ManyToManyField(User,related_name="following")
    follows = models.ManyToManyField(User,related_name="follows")

class Post(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="profile_of_poster",default=None)
    content = models.TextField()
    time = models.DateTimeField()
    likes = models.ManyToManyField(User,related_name="likes")
    edited = models.BooleanField(default=False)
    
    
class Comment(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    content = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="commented_post",default=None)