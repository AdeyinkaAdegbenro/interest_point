import json
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from .models import InterestPoint, SharedInterest

# Create your tests here.
class PointsTestcase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='secret'
        )
        self.client.login(username=self.user.username, password='secret')

        self.interest_point = InterestPoint.objects.create(
            name='Snake Temple',
            longitude='23.45666',
            latitude="23.4454565",
            user=self.user
        )

    def tearDown(self):
        self.user.delete()
        self.interest_point.delete()

    def test_create_interest_point(self):
        load = json.dumps({
            'latitude': '23.45666',
            'longitude': '23.4454565',
            'name': "National Park"
        })
        resp = self.client.post('/index', load, content_type="application/json")
        self.assertEqual(resp.status_code, 201)

        data = resp.json()
        
        interest_point = InterestPoint.objects.get(pk=data['id'])
        self.assertEqual(interest_point.name, 'National Park')
        self.assertEqual(interest_point.longitude, '23.4454565')
        self.assertEqual(interest_point.latitude, '23.45666')
        self.assertEqual(interest_point.user, self.user)

    def test_get_interest_point(self):
        resp = self.client.get('/index')
        expected = [{'id': self.interest_point.id, 'name': 'Snake Temple',
                     'longitude': '23.45666', 
                     'latitude': '23.4454565', 
                     'user': {'id': self.user.id, 
                              'username': 'testuser'
                              }
                    }]
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertCountEqual(expected, data)

    def test_update_interest_point(self):
        load = json.dumps({
            'latitude': '23.45666',
            'longitude': '23.4454565',
            'name': "National Theatre",
            'id': 2
        })
        resp = self.client.post('/index', load, content_type="application/json")
        self.assertEqual(resp.status_code, 201)

        data = resp.json()
        
        interest_point = InterestPoint.objects.get(pk=data['id'])
        self.assertEqual(interest_point.name, 'National Theatre')
        self.assertEqual(interest_point.longitude, '23.4454565')
        self.assertEqual(interest_point.latitude, '23.45666')
        self.assertEqual(interest_point.user, self.user)

    def test_string_representation(self):
        self.assertEqual(str(self.interest_point), 'Snake Temple')

    def test_get_other_users(self):
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            password='secret'
        )
        expected = [{
            'id': self.user2.id,
            'username': 'testuser2'}]
        resp = self.client.get('/users')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertCountEqual(expected, data)

    def test_share_with_user(self):
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            password='secret'
        )
        print(self.interest_point.id, self.user2.id)
        load = json.dumps({'interest_id': self.interest_point.id, 'shared_user': self.user2.id})
        resp = self.client.post('/share', load, content_type="application/json")
        data = resp.json()
        shared_interest = SharedInterest.objects.get(pk=data['id'])
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['interest']['id'], shared_interest.interest.id)
        self.assertEqual(data['shared_user']['id'], shared_interest.shared_user.id)
        self.assertEqual(self.user2, shared_interest.shared_user)
        self.assertEqual(self.interest_point, shared_interest.interest)


