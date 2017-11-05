from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

from crank.views import *
from crank.models import *

class TestRating(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='test', email='test@columbia.edu', password='testpassword')

        self.course = Course_Listing_Table.objects.create(coursenumber="COMSW4156", coursetitle="Advanced Software Engineering")
        self.faculty = Faculty_Table.objects.create(facultyname="TEST FACULTY")
        Course_Faculty_Table.objects.create(course=self.course, faculty=self.faculty) 

    def testSubmitRating(self):
        client = Client()
        response = client.post('/login/', {'username':'test', 'password':'testpassword'})

        course_pair = Course_Faculty_Table.objects.get(course=self.course, faculty=self.faculty)
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 2,
                     "lecture_quality": 1,
                     "overall_quality": 1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}
        response = client.post('/rank/', data=form_data)

        rating = Rating_id.objects.get(course=course_pair)
        self.assertEqual(rating.usefulness, 2)
        self.assertEqual(rating.lecture_quality, 1)
        self.assertEqual(rating.overall_quality, 1)
        self.assertEqual(rating.oral_written_tests_helpful, 1)
        self.assertEqual(rating.learned_much_info, 1)

    def testSubmitDuplicateRating(self):
        client = Client()
        response = client.post('/login/', {'username':'test', 'password':'testpassword'})

        course_pair = Course_Faculty_Table.objects.get(course=self.course, faculty=self.faculty)
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 2,
                     "lecture_quality": 1,
                     "overall_quality": 1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}
        response = client.post('/rank/', data=form_data)

        response = client.post('/rank/', data=form_data)
        self.assertEqual(response.status_code, 400)

    def testSubmitRatingInvalidForm(self):
        client = Client()
        response = client.post('/login/', {'username':'test', 'password':'testpassword'})

        course_pair = Course_Faculty_Table.objects.get(course=self.course, faculty=self.faculty)
        form_data = {"course_faculty_pair": "",
                     "usefulness": 2,
                     "lecture_quality": 1,
                     "overall_quality": -1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}
        response = client.post('/rank/', data=form_data)

        rating = Rating_id.objects.all()
        self.assertEqual(len(rating), 0)

