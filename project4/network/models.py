from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,related_name="poster")
    content = models.TextField()
    time = models.DateTimeField()
    
    
class Comment(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    content = models.TextField()
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="liker")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="liked_post")
      

class Profile(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,related_name="person")
    dp = models.URLField(default=None)
    following = models.ManyToManyField(User,related_name="following")
    follows = models.ManyToManyField(User,related_name="follows")
    
