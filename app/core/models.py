"""
Database models for the core application.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    )

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a User with the given email and password."""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign the custom manager to the User model
    objects = UserManager()

    USERNAME_FIELD = 'email'