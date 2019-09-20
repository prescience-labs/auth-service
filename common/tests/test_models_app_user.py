from django.test import TestCase

from common.models import AppUser

class AppUserModelTests(TestCase):
    def test_create_app_user_works(self):
        user = AppUser.objects.create(provider_id='1')
        self.assertIsInstance(user, AppUser)
