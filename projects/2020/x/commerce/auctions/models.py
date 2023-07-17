from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime    

class User(AbstractUser):
    pass
class Auction(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('fashion', ' Fashion'),
        ('personalCare', 'Personal Care'),
        ('software', 'Software'),
        ('home', 'Home and Kitchen'),
        ('electronics', 'Electronics'),
        ('book', 'Book'),
        ('others', 'Others'),
        ('Default Category', 'Default Category')
        
        # Add more categories as needed
    ]
    name = models.CharField(max_length=64)
    price = models.IntegerField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    imageUrl = models.URLField(blank=True)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)  # Add timestamp field
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='default')
    
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

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ManyToManyField(Auction)

    def __str__(self):
        return f"{self.user.username} - {self.auction.name}"

