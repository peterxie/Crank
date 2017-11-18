from django.test import TestCase
from crank.forms import *

from django.contrib.auth.hashers import check_password, make_password


NEW_PW = "testpassword2"
OLD_PW = "testpassword"

class TestChangePasswordForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='test', email='test@columbia.edu', password='testpassword')

    def testValidForm(self):
        form_data = { "old_password": OLD_PW,
                      "new_password1": NEW_PW,
                      "new_password2": NEW_PW }

        form = ChangePasswordForm(form_data)
        self.assertTrue(form.is_valid())

        old_password, new_password = form.clean_password()

        self.assertEqual(old_password, OLD_PW)
        self.assertEqual(new_password, NEW_PW)

        form.save(self.user.username, old_password, new_password)
        user = User.objects.get(username = self.user.username)
        self.assertTrue(check_password(NEW_PW, user.password))


    def testInvalidPassword(self):
        form_data = { "old_password": NEW_PW,
                      "new_password1": NEW_PW,
                      "new_password2": NEW_PW }

        form = ChangePasswordForm(form_data)
        self.assertTrue(form.is_valid())

        old_password, new_password = form.clean_password()
        try:
            form.save(self.user.username, old_password, new_password)
            self.fail("Failed to verify existing password!")
        except Exception as e:
            self.assertEqual(e.code, 'incorrect_password')

    def testMismatchingPasswords(self):
        form_data = { "old_password": NEW_PW,
                      "new_password1": OLD_PW,
                      "new_password2": NEW_PW }

        form = ChangePasswordForm(form_data)
        self.assertTrue(form.is_valid())

        try:
            old_password, new_password = form.clean_password()
            self.fail("Failed to verify matching password fields")
        except Exception as e:
            self.assertEqual(e.code, 'password_mismatch')


