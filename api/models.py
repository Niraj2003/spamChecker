from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    username = models.CharField(max_length=1, unique=False)
    REQUIRED_FIELDS = ['phone_number']

    # Define related_name to avoid clashes with default User model
    groups = models.ManyToManyField(Group, related_name='api_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='api_user_permissions')

    class Meta:
        swappable = 'auth.User'

class Contact(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    spam_count = models.IntegerField(default=0)

