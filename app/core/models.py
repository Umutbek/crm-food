from django.db import models

from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, PermissionsMixin

from django.conf import settings


class Role(models.Model):
    """Model for role"""
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an Email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email instead of username"""
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=100, unique=True, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Department(models.Model):
    """Model for Department"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MealCateg(models.Model):
    """Model for MealCategory"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    name = models.CharField(max_length=100)
    depid = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name


class Meal(models.Model):
    """Model for Meals"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True

    )
    name = models.CharField(max_length=100)
    category = models.ForeignKey(MealCateg, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
