from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone, safestring


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_superuser):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            password=password,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password):
        return self._create_user(email, password, is_superuser=False)

    def create_superuser(self, email, password):
        return self._create_user(email, password, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"

    objects = UserManager()

    email = models.EmailField(unique=True)
    subscriptions = models.ManyToManyField(
            "rack.Comic", blank=True, related_name='users')
    last_read = models.DateTimeField(default=timezone.now)
