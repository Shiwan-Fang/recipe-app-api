"""
Test for models in the core app.
"""

from django.test import TestCase  # base class for tests
from django.contrib.auth import get_user_model  # helper function to get the default user model

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password)
        
        self.assertEqual(user.email, email)
        # check the password through hashing system, not direct comparison
        self.assertTrue(user.check_password(password))