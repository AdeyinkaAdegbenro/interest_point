from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import InterestPoint

# Create your tests here.
class PointsTestcase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='secret'
        )

        self.interest_point = InterestPoint.objects.create(
            name='Snake Temple',
            longitude='23.45666',
            latitude=self.user,
            user=self.user
        )

    def test_create_interest_point(self):
        response = self.client.get('/index')

    def test_get_interest_point(self):
        pass

    def test_update_interest_point(self):
        pass

    def test_string_representation(self):
        self.assertEqual(self.interest_point, 'Snake Temple')