from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class TimeStampModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    otp= models.IntegerField(blank=True, null=True)
    otpVerified= models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.username



    

