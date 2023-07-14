"""
Django command to wait for the database to be available.
"""
import time  # used to make execution sleep

# error thrown when db is not ready
from psycopg2 import OperationalError as Psycopg2OpError

# error that Django throws when db is not ready
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):  # standard syntax for any command
        """Entrypoint for command."""

        # stdout: standard output used to log things
        # to the screen (console) as our command is executing.
        self.stdout.write('Waiting for database...')

        # define a boolean to false, assuming that db is not up
        # until it catches that it is
        db_up = False

        # track if db is up yet (raises no exceptions, then returns True)
        while db_up is False:
            try:
                # call check method that we mock inside our tests
                self.check(databases=['default'])
                db_up = True
            # catch exceptions (errors)
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)  # pause for 1 second

        # once db_up = True
        self.stdout.write(self.style.SUCCESS('Database available!'))
