from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True )


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class UserIpAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def addIpaddress(self, address):
        self.address = address
        self.save()


