from django.contrib.auth import get_user_model
from django.test import TestCase

from common.models import User

CustomUser = get_user_model()

class UserModelTests(TestCase):
    def test_create_user_works(self):
        user = User.objects.create(
            email='test@example.com',
            password='testPassword1',
        )
        self.assertIsInstance(user, User)
