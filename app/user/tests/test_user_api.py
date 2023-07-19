"""
Tests for the user API.
"""

# docker-compose run --rm app sh -c "python manage.py test"

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# Add api url that we'll be testing
# returns full url path inside our project
# user as app, create as endpoint
CREATE_USER_URL = reverse('user:create')
# url endpoint for creating tokens in our user API
TOKEN_URL = reverse('user:token')


# Add a helper function to create a user for testing
# **params: passes in any dict that contains params and
# can be called straight into the user
def create_user(**params):
    """Create and returna a new user with details passed by parameters."""
    return get_user_model().objects.create_user(**params)


# Add a test class
class PublicUserApiTests(TestCase):
    """Test the public fetures of the user API."""

    def setUp(self):
        # creates an API Client that is used for testing
        self.client = APIClient()

    # Add a test method to the test class
    def test_create_user_success(self):
        """Test creating a user is successfull."""

        # payload that is posted to API to test (register new user info)
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # post the payload data to the API url
        res = self.client.post(CREATE_USER_URL, payload)

        # check that the endpoints returns HTTP 201 CREATED response
        # (success response code for creating objects in the db via an API)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve the object from the db with the email address
        # that we passed in as the payload.
        user = get_user_model().objects.get(email=payload['email'])

        # Validate that the object was actually created
        # in the db after we did the post.
        # If the user was created successfuly, the user will be
        # returned to the user variable. Then, we can check password
        # method on our user and pass in the clear text password
        # that we gave in the payload in order to check that
        # this assets "true", which means that the password is correct.
        self.assertTrue(user.check_password(payload['password']))

        # Ensure that the password or the password hash
        # is not returned in the response, bcs this is a security issue
        # and all the password check is done in the db.
        # Checks if there's a key 'password' returned to the user
        self.assertNotIn('password', res.data)

    # check that creating a user with email that is alredy in the db won't work
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)  # created a new user (func defined above)

        # make post request
        res = self.client.post(CREATE_USER_URL, payload)

        # check that we get a bad response back
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # check if password is too short and if user email is in db
    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # search a user by the email address provided
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()  # exists(): returns T/F depending on whether user exists

        # confirm that user doesN'T exist in the db
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""

        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        # create a new user with user_details
        create_user(**user_details)

        # sent to token API to log in
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        # post payload to token url
        res = self.client.post(TOKEN_URL, payload)

        # check that response includes a token
        self.assertIn('token', res.data)
        # check that response status code is HTTP 200 OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""

        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        # check that token is not in db bcs it has wrong credentials
        self.assertNotIn('token', res.data)
        # check that request is bad bcs login is supposed to be unsuccessful
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""

        # pass in a blank password
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        # check that token is not in db bcs it has wrong credentials
        self.assertNotIn('token', res.data)
        # check that request is bad bcs login is supposed to be unsuccessful
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
