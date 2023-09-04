# ensure to remove emty whitespace in a code by:
# go to VS File -> Preferences -> Settings ->
# search whitespace -> check the checkbox "Trim Trailing Whitespace"
# to test the code in the terminal:
# docker-compose run --rm app sh -c "python manage.py test"

"""
Tests for models.
"""
# patch: to replace behavior for testing purposes
from unittest.mock import patch

# provides assertion methods like assertEqual, assertTrue, assertRaises
from django.test import TestCase

# Helps to get reference to your custom user model.
# https://docs.djangoproject.com/en/3.2/topics/
# auth/customizing/#django.contrib.auth.get_user_model
# Goes to UserManager. Helper function to get the dafault user model,
# which will then be automatically updated if you make changes to it
from django.contrib.auth import get_user_model  # only for user model

# used for storing one of the values of our recipe object
from decimal import Decimal

from core import models
from core.models import UserProfile


# helper function for creating a test user
def create_user(email='user@example.com', password='testpass123'):
    """Create and reurn a new user."""
    return get_user_model().objects.create_user(email, password)


# test that checks that we can create a user with email
class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'  # @example.com is reserved for testing
        password = 'testpass123'

        # get_user_model: get the user model
        # objects: reference to the UserManager that we created in modelspy
        # create_user: method, passing email and password
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        # check if emails match
        self.assertEqual(user.email, email)

        # check if password is correct
        # check_password: method by dafault baseusermanager
        # to check password through a hashing system
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        # create a list of email adresses
        sample_emails = [
            # [email adress, expected email adress after registering]
            # Note: could be any size @ has to be normalized to lowercase
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        # make sure emails are normalized after the user model was created
        for email, expected in sample_emails:
            # create a user with one of the emails at a time and password
            user = get_user_model().objects.create_user(email, 'sample123')
            # make sure that the user email is equal to the expected email
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""

        # test if create_user method raises an exception
        # when we provide an empty email
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""

        # create_superuser: method to create superusers
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        # field provided by PermissionsMixin
        self.assertTrue(user.is_superuser)
        # is_staff: comes from User class in models.py
        self.assertTrue(user.is_staff)  # allows to login into Django Admin

    def test_create_profile(self):
        """Test creating a bio in user profcile successful."""

        # create a user to assign to our recipe objects
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        user_profile = UserProfile.objects.create(
            user=user,
            picture=None,  # Replace with an actual image file if needed
            bio="Test bio",
            dob="2022-01-01",
            pronouns=UserProfile.SHE,
            gender=UserProfile.FEMALE
        )

        self.assertEqual(user_profile.user, user)
        self.assertEqual(str(user_profile), f'{user_profile.user.email} Profile')

    def test_create_recipe(self):
        """Test creating a recipe is successful."""

        # create a user to assign to our recipe objects
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        # create a recipe
        recipe = models.Recipe.objects.create(
            user=user,  # a user that recipe belongs to
            title='Sample recipe name',  # title of a recipe
            time_minutes=5,  # minutes it takes to make a recipe
            # rough price of what it costs to make a recipe
            price=Decimal('5.50'),  # Note: integer is better for currency
            description='Sample recipe description.',  # description of recipe
        )

        # check if title is represented as string
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""

        # create a user to assign to our recipe objects
        user = create_user()

        # create a recipe
        tag = models.Tag.objects.create(
            user=user,  # a user that tag belongs to
            name='Tag1',  # name of a tag
        )

        # check if tag.name is represented as string
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()

        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1',
        )

        # check if tag.name is represented as string
        self.assertEqual(str(ingredient), ingredient.name)

    # add decorator to patch uuid func that will be imported to models
    # Reason: to replace behavior of uuid (instead of unique identifier)
    @patch('core.models.uuid.uuid4')
    # uuid: unique identifier for the uploading file (images)
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""

        uuid = 'test-uuid'  # mocked response
        # set return value to uuid string
        mock_uuid.return_value = uuid
        # recipe_image_file_path: generates path to the uploaded image
        # None: replaces the instance
        # example.jpg: original name of the uploaded
        file_path = models.image_file_path(None, 'example.jpg')

        # check that result of function keeps same extentition
        # uploads/recipe/{uuid}.jpg, replaces "example" with {uuid},
        # and stored in uploads/recipe/
        self.assertEqual(file_path, f'uploads/nonetype/{uuid}.jpg')

