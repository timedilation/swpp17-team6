from django.test import TestCase, Client
from .models import UserInfo
from location.models import getLocationFromCSVFile, LocationL1, LocationL2, LocationL3
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json

class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        getLocationFromCSVFile ('./location/korea.CSV')

        client = Client(enforce_csrf_checks = True)
        response = client.get('/api/user/token')
        csrftoken = response.cookies['csrftoken'].value
        response = self.client.post(
                '/api/user/signup',
                json.dumps({
                    'email': 'PlaskTest1@snu.ac.kr',
                    'username': 'PlaskTest1',
                    'password': '123123',
                    'locations': 'South Korea/Busan/Buk;South Korea/Busan/Busanjin;',
                    'services': 'coffee;pizza;',
                    'blockedServices': 'asdf;qwer',
                    'notiFrequency': '10'
                    }),
                content_type = 'application/json',
                HTTP_X_CSRFTOKEN = csrftoken)

        response = self.client.post('/api/user/signin', json.dumps({'email': 'PlaskTest1@snu.ac.kr', 'password': '123123'}), content_type = 'application.json')
        self.assertEqual(response.status_code, 204)

    def test_signin_failed(self):
        response = self.client.post('/api/user/signin', json.dumps({'email': 'PlaskTest1', 'password': '123123'}), content_type = 'application.json')

    def test_userinfo_get(self):
        userinfo = User.objects.get(username = 'PlaskTest1@snu.ac.kr').userinfo
        response = self.client.get('/api/user/userinfo')
        data = json.loads(response.content.decode())
        self.assertEqual (response.status_code, 200)
        self.assertEqual (data['locations'], 'South Korea/Busan/Buk;South Korea/Busan/Busanjin;')
        self.assertEqual (data['username'], 'PlaskTest1')
        self.assertEqual (data['services'], 'coffee;pizza;')
        self.assertEqual (data['blockedServices'], 'asdf;qwer;')
        self.assertEqual (int(data['notiFrequency']), 10)

    def test_userinfo_put(self):
        response = self.client.put(
                '/api/user/userinfo',
                json.dumps({
                    'password': '456456',
                    'locations': 'South Korea/Busan/Buk;South Korea;South Korea/Seoul;',
                    'services': 'coffee;pizza;microsoft;hell;swpp',
                    'blockedServices': 'zxcv;qwer;bnmg;asdf',
                    'notiFrequency': '15'
                    }),
                content_type = 'application/json'
                )
        self.assertEqual (response.status_code, 204)
        userinfo = User.objects.get(username = 'PlaskTest1@snu.ac.kr').userinfo
        serv = list(userinfo.services.all())
        block = list(userinfo.blocked.all())
        loc = list(userinfo.locations.all())

        self.assertEqual (len(serv), 5)
        self.assertEqual (len(block), 4)
        self.assertEqual (len(loc), 3)
        self.assertEqual (userinfo.notify_freq, 15)
        self.assertEqual (str(loc[0].loc_code1) + '/' + str(loc[0].loc_code2) + '/' + str(loc[0].loc_code3), '213/1/1')
        self.assertEqual (str(loc[1].loc_code1) + '/' + str(loc[1].loc_code2) + '/' + str(loc[1].loc_code3), '213/-1/-1')
        self.assertEqual (str(loc[2].loc_code1) + '/' + str(loc[2].loc_code2) + '/' + str(loc[2].loc_code3), '213/16/-1')


    def test_get_loc_list(self):
        response = self.client.get('/api/location/countries', content_type = 'application.json')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
#		print(data)
        response = self.client.get('/api/location/South Korea', content_type = 'application.json')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
#		print(data)
        response = self.client.get('/api/location/South Korea/Seoul', content_type = 'application.json')
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.post('/api/user/signout', content_type = 'application.json')
        self.assertEqual(response.status_code, 405)
        response = self.client.get('/api/user/signout', content_type = 'application.json')
        self.assertEqual(response.status_code, 204)

    def test_signup_with_duplicate_email(self):
        self.client = Client()
        client = Client(enforce_csrf_checks = True)
        response = client.get('/api/user/token')
        csrftoken = response.cookies['csrftoken'].value
        response = self.client.post('/api/user/signup',
                json.dumps({
                    'email': 'PlaskTest1@snu.ac.kr',
                    'username': 'PlaskTest1',
                    'password': '123123',
                    'locations': 'South Korea/Busan/Buk;South Korea/Busan/Busanjin;',
                    'services': 'coffee;pizza;',
                    'blockedServices': 'asdf;qwer',
                    'notiFrequency': '10'
                    }),
                content_type = 'application/json',
                HTTP_X_CSRFTOKEN = csrftoken)
        self.assertEqual(response.status_code, 401)

