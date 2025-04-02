from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_login = models.DateTimeField(null=True, blank=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    telegram_username = models.CharField(max_length=30, blank=True, null=True)

