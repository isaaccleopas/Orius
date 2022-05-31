from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager

# Create your models here.

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=100, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    bio = models.TextField(max_length=200, blank=True, null=True, default="")
    designation = models.CharField(max_length=100, blank=True, null=True, default="")
    location = models.CharField(max_length=50, blank=True, null=True, default="")
    age = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
                              
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=20,
                                    error_messages={
                                        'unique': "A user with that phone number already exists."
                                    })
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()