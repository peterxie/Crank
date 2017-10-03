from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import index, signUp
from .models import User

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')

        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        request = self.factory.post('/signUp', {'inputName': 'testName', 'inputEmail':'testEmail', 'inputPassword':'testPassword'})
        request.user = AnonymousUser()
        response = signUp(request)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(name='testName')
        print(user)
        self.assertEqual(user.userName, 'testEmail')
        self.assertEqual(user.password, 'testPassword')

