from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Can be extended with additional fields as needed.
    """
    pass

    def __str__(self):
        return self.username
