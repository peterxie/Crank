from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

from crank.views import *
from crank.models import *

v1 = "fp12345"  # valid uni
v2 = "Alpha"  # valid first or last
v3 = "Qwerty12345"  # valid password
v4 = "Qwerty12345"  # valid password


class TestAccountCreate(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def testUni_FirstTwoCharactersAreLetters(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        print('testUni_FirstTwoCharactersAreLetters')
        #print('uni is ', v1)
        #print('uni[0] is ', v1[0])
        #print('uni[1] is ', v1[1])

        self.assertEqual(v1[0].isalpha() and v1[1].isalpha(), True, msg="UNI does not begin with two characters")

    def testUni_LengthOfSix(self):
        v1 = "fp1234"  # valid uni
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        print('testUni_LengthOfSix')
        #print('uni is ', v1)
        #print('length of uni is ', len(v1))
        self.assertEqual(len(v1), 6, msg="UNI does not have a length of 6 characters")

    def testUni_LengthOfSeven(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        print('testUni_LengthOfSeven')
        #print('uni is ', v1)
        #print('length of uni is ', len(v1))
        self.assertEqual(len(v1), 7, msg="UNI does not have a length of 7 characters")

    def testUni_PasswordsMatch(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v4}
        response = client.post('/signup/', data=form_data)
        print('testUni_PasswordsMatch')
        #print('Password 1 is ', v3)
        #print('Password 2 is ', v4)
        self.assertEqual(v3 == v4, True, msg="Passwords do not match")

    def testSignUpValid(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        print('test_signupvalid')
        print(response)
        self.assertEqual(response.status_code, 302)  # 302 is valid, 200 invalid