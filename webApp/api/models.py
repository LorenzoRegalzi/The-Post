from datetime import datetime
import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from api.utils import sendTransaction


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)



    def publish(self):
        
        self.published_date = timezone.now()
        

    def __str__(self):
        return self.title

    def writeOnChain (self): 
        self.hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        

class UserIpAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def add_ip_address(self, address):
        self.address = address
        self.save()


