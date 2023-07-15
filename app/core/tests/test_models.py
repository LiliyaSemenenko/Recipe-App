# ensure to remove emty whitespace in a code by:
# go to VS File -> Preferences -> Settings -> search whitespace -> check the checkbox "Trim Trailing Whitespace"

"""
Tests for models.
"""

from django.test import TestCase
# helps to get reference to you custom user model
from django.contrib.auth import get_user_model  # helper function to get the dafault user model, which will then be automatically updated if you make changes to it

# test that checks that we can create a user with email
class ModelTests(TestCase):
    """Test models."""

    def test_carete_user_with_email_siccessful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com' # @example.com is reserved for testing
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
        # check_password: method by dafault baseusermanager to check password through a hashing system
        self.assertTrue(user.check_password(password))

