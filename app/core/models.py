"""
Database models.
"""
import uuid  # to generate uuid
import os  # for file path management functions

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

# instance: of the object that the image is being uploaded to
# filename:name of original file that's being uploaded
def image_file_path(instance, filename):
    """Generate file path for new recipe image."""

    model_class = instance.__class__.__name__

    # extract the extention of a filename
    ext = os.path.splitext(filename)[1]
    # create own filename with uuid and keep the original extenetion
    filename = f'{uuid.uuid4()}{ext}'

    # Create a URL path for an image
    # os.path.join(): ensures that string created in format for
    # operating system that's running on
    return os.path.join('uploads', model_class.lower(), filename)


# https://docs.djangoproject.com/en/3.2/topics/auth/customizing
# /#writing-a-manager-for-a-custom-user-model
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


# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#auth-custom-user
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

    # replace username field with a custom email field
    USERNAME_FIELD = 'email'


class UserProfile(models.Model):

    # # RELATIONSHIP
    # user = models.ForeignKey(
    #     to = User,
    #     on_delete = models.CASCADE,
    #     related_name = "user_account"
    # )

    # # DATABASE FIELDS
    # first_name = models.ForeignKey(User, to_field="firstname_field", verbose_name="First Name")
    # last_name = models.ForeignKey(User, to_field="lastname_field", verbose_name="Last Name")

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    SHE = 'SHE'
    HE = 'HE'
    THEY = 'THEY'
    CUSTOM = 'CUSTOM'
    NONE = 'NONE'

    FEMALE = 'FEMALE'
    MALE = 'MALE'

    PRONOUNS = [
        (SHE, "She/Her"),
        (HE, "He/Him"),
        (THEY, "They/Them"),
        (CUSTOM, "Custom"),
        (NONE, "Prefer not to say"),
    ]
    GENDER = [
        (FEMALE, "Female"),
        (MALE, "Male"),
        (CUSTOM, "Custom"),
        (NONE, "Prefer not to say"),
    ]

    picture = models.ImageField(null=True, upload_to=image_file_path)
    bio = models.CharField(max_length=225)
    # private info
    dob = models.DateField()

    pronouns = models.CharField(
        max_length=20,
        choices=PRONOUNS,
        default=NONE,
    )

    # private info
    gender = models.CharField(
        max_length=20,
        choices=GENDER,
        default=NONE,
    )

    # once we create a new feed item automatically add the date time stamp that the item was created
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} Profile' #show how we want it to be displayed


class Recipe(models.Model):  # models.Model: Django base class
    """Recipe object."""

    # create fields for recipe class

    # set user that recipe belongs to
    # ForeignKey: sets up a relationship btw
    # recipe model and another model (AUTH_USER_MODEL here)
    # It links each recipe to a specific user, and since it's a ForeignKey,
    # it is required to have a value pointing to a valid user.
    user = models.ForeignKey(  # REQUIRED field
        settings.AUTH_USER_MODEL,
        # if related object (user) is deleted,
        # recepies associated to him will also be deleted
        on_delete=models.CASCADE,
    )
    # CharField without blank=True means it must have a non-empty value
    title = models.CharField(max_length=255)  # REQUIRED field

    # time to create a recipe
    # IntegerField is required and must have a value.
    time_minutes = models.IntegerField()  # REQUIRED field

    # price of a recipe
    # DecimalFieldis required and must have a value.
    # REQUIRED field
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # TextField: holds more and a variety of content than CharField
    # Note: with some db systems (MySQL), TextField may be worse at performance
    description = models.TextField(blank=True)  # NOT REQUIRED (blank=True)

    # external link to the recipe
    link = models.CharField(max_length=225, blank=True)  # NOT REQUIRED

    # tags can be associated to many recepies and vice versa
    tags = models.ManyToManyField('Tag')  # NOT REQUIRED

    # ingrediens can be associated to many recepies and vice versa
    ingredients = models.ManyToManyField('Ingredient')  # NOT REQUIRED

    # Note: recipe_image_file_path is a reference to a func, not calling it
    # That's how you specify the path you want to upload files to
    # NOT REQUIRED
    image = models.ImageField(null=True, upload_to=image_file_path)

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
