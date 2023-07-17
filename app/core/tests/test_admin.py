# In the terminal: docker-compose run --rm app sh -c "python manage.py test"
# start development server: docker-compose up
# url: http://127.0.0.1:8000/admin/

"""
Tests for the Django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#overview-and-a-quick-example

class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    # setups up modules that we add to this class and runs before any other test
    def setUp(self):
        """Create user and client."""

        self.client = Client() # django test client that allows to make http requests

        # creates a admin user with create_superuser()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )

        # force authentication with admin_user
        self.client.force_login(self.admin_user)

        # creates a regular user with create_user()
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
        )


    def test_users_lists(self):
        """Test that users are listed on page."""

        # get the usrl for the changelist (list of users in the system)
        url = reverse('admin:core_user_changelist') # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls

        # bcs of forsed login, then it will get authenticated as the admin user
        res = self.client.get(url) # http get request to the url


        # check that the page contains the name of the user we created
        self.assertContains(res, self.user.name)

        # checks that the page contains email of the user we created
        self.assertContains(res, self.user.email)


    def test_edit_user_page(self):
        """Test the edit user page works."""

        # http://127.0.0.1:8000/admin/core/user/id/change/
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # check that page loads successfullt with http 200 response
        self.assertEqual(res.status_code, 200)


    def test_create_user_page(self):
        """Test the create user page works."""

        url = reverse('admin:core_user_add') # no id bcs we're creating a new user
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)