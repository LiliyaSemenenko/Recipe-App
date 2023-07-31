"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


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


class Recipe(models.Model):  # models.Model: Django base class
    """Recipe object."""

    # create fields for recipe class

    # set user that recipe belongs to
    # ForeignKey: sets up a relationship btw
    # recipe model and another model (AUTH_USER_MODEL here)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # if related object (user) is deleted,
        # recepies associated to him will also be deleted
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    # TextField: holds more and a variety of content than CharField
    # Note: with some db systems (MySQL), TextField may be worse at performance
    description = models.TextField(blank=True)
    # time to create a recipe
    time_minutes = models.IntegerField()
    # price of a recipe
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # external link to the recipe
    link = models.CharField(max_length=225, blank=True)
    # tags can be associated to many recepies and vice versa
    tags = models.ManyToManyField('Tag')

    # returns string representation of an object (title here)
    # If not sepcified, in Django Admin you'll see ID instead of a title
    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tags for filtering recipes."""

    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            # if related object (user) is deleted,
            # tags associated to him will also be deleted
            on_delete=models.CASCADE,
        )
    name = models.CharField(max_length=255)

    # returns string representation of an object (name here)
    # If not sepcified, in Django Admin you'll see ID instead of a name
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredients for recipes."""

    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            # delete ingredients if associated user was deleted
            on_delete=models.CASCADE,
        )

    name = models.CharField(max_length=225)

    # returns string representation of an ingredient name
    def __str__(self):
        return self.name
