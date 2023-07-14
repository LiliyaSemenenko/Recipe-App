"""
Test custom Django management commands.
"""

# In terminal: docker-compose run --rm app sh -c "python manage.py test"

from unittest.mock import patch  # patch to mock behavior of db

# OperationalError is an error that we might get when connecting to db
# before it's ready (hasn't started and can't accept connections)
from psycopg2 import OperationalError as Psycopg2OpError

# call_command simulates calling command by the name
from django.core.management import call_command

# raised when db is ready to accept connections,
# BUT has NOT created dev db that we want to use
from django.db.utils import OperationalError

# base test class used for unittest
# (we don't need migrations so no need for db setup)
from django.test import SimpleTestCase

""" mock the behavior (command in '') of db
# path: core.management.commands.wait_for_db
# base class in wait_for_db.py: Command
# check method to check the status of db: check """


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # test case #1: db is READY
    # patched_check: object that is defined aboves
    # (used to custumize the behaviour)
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""

        # when calling "check" (line 16) inside our test case, return True
        patched_check.return_value = True

        """ execute the code inside wait_for_db.py
        # checks if db is ready
        # checks if the command is set up correctly and can be called """
        call_command('wait_for_db')

        # test if "check" method has been called
        # with databases=['default'] parameters
        patched_check.assert_called_once_with(databases=['default'])

    # mark the sleep method
    # check the db, then call sleep to wait for some time before checking again
    # Note: since it's mocking, it won't actually make us wait during execution
    @patch('time.sleep')
    # test case #2: db is NOT READY, so delay
    # Note: oder of patch args starts from lower located patch to the top patch
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""

        """ Mocking setup when raising exception
        # Exception is raised when db is NOT ready
        # the first 2 times, vcall the mock method, so raise Psycopg2OpError
        # slash: is used to break the line
        # then raise 3 OperationalError
        # on the 6th time we call it, return True """
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # test if number of calls of check method is 6
        self.assertEqual(patched_check.call_count, 6)
        """ test if "check" method is called with correct paarmeters
        # Note: here awe use ssert_called_WITH bcs of calling 6 times
        # (more than 1) while on like 36, assert_called_ONCE_with """
        patched_check.assert_called_with(databases=['default'])
