from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime    


class User(AbstractUser):
    pass

class Auction(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    imageUrl = models.URLField(blank=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)  # Add timestamp field

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete= models.CASCADE)
    bid = models.IntegerField(max_length=10)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)  # Add timestamp field

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete= models.CASCADE)
    comment = models.TextField(max_length=150)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now,blank=True)  # Add timestamp field
