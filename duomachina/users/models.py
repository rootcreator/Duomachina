from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_artist = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.username
