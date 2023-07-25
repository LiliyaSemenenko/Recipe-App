# ensure to remove emty whitespace in a code by:
# go to VS File -> Preferences -> Settings ->
# search whitespace -> check the checkbox "Trim Trailing Whitespace"
# to test the code in the terminal:
# docker-compose run --rm app sh -c "python manage.py test"

"""
Tests for models.
"""
# provides assertion methods like assertEqual, assertTrue, assertRaises
from django.test import TestCase
# Helps to get reference to you custom user model.
# Goes to UserManager. Helper function to get the dafault user model,
# which will then be automatically updated if you make changes to it
from django.contrib.auth import get_user_model  # only for user model

# used for storing one of the values of our recipe object
from decimal import Decimal

from core import models


# test that checks that we can create a user with email
class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'  # @example.com is reserved for testing
        password = 'testpass123'

        # get_user_model: get the user model
        # objects: reference to the manager that we create
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
