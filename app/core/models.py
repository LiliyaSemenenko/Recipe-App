"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# define UserManage based of BaseUserManager class provided by Django
class UserManager(BaseUserManager):
    """Manager for users."""

    # Create a create_user method below
    # (make sure create_user is spelled exactly like this)
    #  **extra_field: allows to pass new values when calling
    #  the model without changing the method itself
    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user"""

        if not email:
            raise ValueError('User must have an email address.')

        # self.model: accessing the model we're associated with
        # (same as defining a new user object)
        # normalize_email: is a mathod provided by BaseUserManager
        #  **extra_field: can provide keyword arguments
        # that will be passed to the model (ex. extra fields)
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # set the encrypted password to a user
        user.set_password(password)

        # save user model
        # self._db: supports adding multiple databses to a project,
        # in case you want to do it later
        user.save(using=self._db)

        # return the user objec
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# AbstractBaseUser: contains functionality for user auth system
# PermissionsMixin:contains functionality for permissions and fields
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    # validates email and ensures it's unique
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=225)
    # registered users' status is active by default
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign UserMnager to this custom user class
    objects = UserManager()

    # replace username field witha custom email field
    USERNAME_FIELD = 'email'
