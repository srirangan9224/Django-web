from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(max_length=1000)
    listing_date = models.DateTimeField(default=datetime.datetime.now())
    listed_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")
    sold = models.BooleanField()
    image = models.URLField(default=None)


class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="watchlister")
    item = models.ManyToManyField(Listing,related_name="watchlisted_item")


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="commented_item")
    comment = models.TextField(max_length=1000)

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    items = models.ManyToManyField(Listing,related_name="items_in_category")