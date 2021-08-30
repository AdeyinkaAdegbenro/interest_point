from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
class AccountsTestcase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )


    def test_sign_up(self):
        pass

    def test_login(self):
        pass

    def test_logout(self):
        pass

    def test_bad_login(self):
        pass

    def test_bad_sign_up(self):
        pass