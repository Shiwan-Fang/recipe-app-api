"""
Test custom Django mangement commands.
"""
from unittest.mock import patch

# one of the errors that can be raised when the database is not available
from psycopg2 import OperationalError as Psycopg2OpError

# a helper function to call a Django management command in our tests
from django.core.management import call_command
# another error that can be raised when the database is not available
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mock the `check` method of the wait_for_db command (basecommand)
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready."""

        # when check is called, it will return True
        patched_check.return_value = True

        # execute the the code inside wait_for_db.py
        call_command('wait_for_db')

        # check the check method has been called
        patched_check.assert_called_once_with(databases=['default'])

    # mock the sleep func, so it doesn't actually pause the test execution
    @patch('time.sleep')
    # the arguments order: the one closest to the function is passed first
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # simulate the check method raising 2 errors few times before true
        patched_check.side_effect = [Psycopg2OpError]*2 + \
            [OperationalError]*3 + [True]
        # execute the the code inside wait_for_db.py
        call_command('wait_for_db')

        # check the check method has been called 6 times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
