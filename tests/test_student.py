from django.contrib.auth.models import User
from django.test import TestCase, Client

from crank.views import *
from crank.models import *

v1 = "ab1234"       #valid uni
v2 = "Alpha"        #valid first or last
v3 = "Qwerty12345"  #valid password
p = 302             #pass
f = 200             #fail

class TestAccountCreate(TestCase):

    def testSignUpValid(self):
        client = Client()
        response = client.get('/signup/')
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p) #302 is valid, 200 invalid

    #Username tests
    def testUsername1_1(self):
        client = Client()
        form_data = {"username": "cd4321",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, 302)
   

    def testUsername1_2(self):
        client = Client()
        form_data = {"username": "c$d255",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)
   
    def testUsername1_3(self):
        client = Client()
        form_data = {"username": "A9C#",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)
   
    def testUsername1_4(self):
        client = Client()
        form_data = {"username": "cde",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)
   
    def testUsername1_5(self):
        client = Client()
        form_data = {"username": "9B1246",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)
   
    def testUsername1_6(self):
        client = Client()
        form_data = {"username": "abc123",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)
   
    def testUsername1_7(self):
        client = Client()
        form_data = {"username": "abc1234",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        print(response)
        self.assertEqual(response.status_code, p)
   
    def testUsername1_8(self):
        client = Client()
        form_data = {"username": "av43213",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)
   
    def testUsername1_9(self):
        client = Client()
        form_data = {"username": "fp236",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        print(response)
        self.assertEqual(response.status_code, f)

    def testUsername1_10(self):
        client = Client()
        form_data = {"username": "fp23641",
                     "first_name": v2,
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)


    #First & Last Name tests
    def testFirstName1_1(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "Frank",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)

    def testFirstName1_2(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "Panettieri",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)


    def testFirstName1_3(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "Frank11357",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testFirstName1_4(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "Panettieri11357",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testFirstName1_5(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "123456789",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testFirstName1_6(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "987654321",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)

    def testFirstName1_7(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "Abcdefghijklmnopqrstuvwxyzabcdefgh",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testFirstName1_8(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": "Abcdefghijklmnopqrstuvwxyzxyzxyzxyz",
                     "last_name": v2,
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testLastName1_1(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "Frank",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)

    def testLastName1_2(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "Panettieri",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)


    def testLastName1_3(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "Frank11357",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testFirstName1_4(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "Panettieri11357",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def LastName1_5(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "123456789",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testLastName1_6(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "987654321",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)

    def testLastName1_7(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "Abcdefghijklmnopqrstuvwxyzabcdefgh",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testLastName1_8(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": "Abcdefghijklmnopqrstuvwxyzxyzxyzxyz",
                     "password1": v3,
                     "password2": v3}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    #Password tests
    def testPassword_1_1(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "M@chin$Lea#nin6",
                     "password2": "M@chin$Lea#nin6"}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)

    def testPassword_1_2(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "M@chin$L",
                     "password2": "M@chin$L"}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testPassword_1_3(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "M@chin$Le",
                     "password2": "M@chin$Le"}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)

    def testPassword_1_4(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "M@chin$Lea",
                     "password2": "M@chin$Lea"}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)


    def testPassword_1_5(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "",
                     "password2": ""}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    #def Password_2(self) - Common Password Validation to be interated through the django list
    #def Password_3(self) - Comparison to see if password in other inputs

    def testPassword_4_1(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "12345678910",
                     "password2": "12345678910"}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, f)

    def testPassword_4_2(self):
        client = Client()
        form_data = {"username": v1,
                     "first_name": v2,
                     "last_name": v2,
                     "password1": "M@chin$Lea",
                     "password2": "M@chin$Lea"}
        response = client.post('/signup/', data=form_data)
        self.assertEqual(response.status_code, p)
   

