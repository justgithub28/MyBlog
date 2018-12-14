from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    username=models.CharField(blank=False,unique=True,max_length=256)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    #USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username',]

    def __str__(self):
        return self.email
