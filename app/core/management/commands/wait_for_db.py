"""
Django command to wait for database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

# error django throws when db is not ready
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        pass
