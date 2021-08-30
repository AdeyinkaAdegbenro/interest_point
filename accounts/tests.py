from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from points.models import InterestPoint, SharedInterest
import json

# Create your tests here.
class AccountsTestcase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='secret'
        )

        self.interest_point = InterestPoint.objects.create(
            name='Snake Temple',
            longitude='23.45666',
            latitude="23.4454565",
            user=self.user
        )

    def tearDown(self):
        self.user.delete()
        self.interest_point.delete()

    def test_login(self):
        self.client.login(username=self.user.username, password='secret')
        resp2 = self.client.get('/index')
        self.assertEqual(resp2.status_code, 200)

    def test_logout(self):
        self.client.login(username=self.user.username, password='secret')
        self.client.logout()
        load = json.dumps({
            'latitude': '23.45666',
            'longitude': '23.4454565',
            'name': "National Park"
        })
        resp2 = self.client.post('/index', load, content_type="application/json")
        self.assertEqual(resp2.status_code, 400)

    def test_bad_login(self):
        self.client.login(username='fakeuser', password='secret')
        resp2 = self.client.get('/index')
        self.assertEqual(resp2.status_code, 400)
