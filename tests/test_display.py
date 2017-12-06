from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

from crank.views import *
from crank.models import *

USEFULNESS_C = 5
LECTURE_QUALITY_C = 4 
OVERALL_C = 3
ORAL_WRITTEN_C = 2
LEARNED_MUCH_C = 1
FACULTY_NAME_C = "TEST FACULTY"
COURSE_NUMBER_1_C = "COMSW4156"
COURSE_NUMBER_2_C = "COMSE6156"

class TestDisplay(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='test', email='test@columbia.edu', password='testpassword')
        self.user_2 = User.objects.create_superuser(username='test2', email='test1@columbia.edu', password='testpassword2')

        self.course_1 = Course_Listing_Table.objects.create(coursenumber=COURSE_NUMBER_1_C, 
                                                            coursetitle="Advanced Software Engineering")
        self.course_2 = Course_Listing_Table.objects.create(coursenumber=COURSE_NUMBER_2_C,
                                                            coursetitle="Advanced Topics in Software Engineering")
        self.faculty = Faculty_Table.objects.create(facultyname=FACULTY_NAME_C)
        self.course_faculty_1 = Course_Faculty_Table.objects.create(course=self.course_1, faculty=self.faculty) 
        self.course_faculty_2 = Course_Faculty_Table.objects.create(course=self.course_2, faculty=self.faculty)


    def testRankDisplay(self):
        client = Client()

        response = client.post('/login/', {'username':'test', 'password':'testpassword'})

        course_pair = Course_Faculty_Table.objects.get(course=self.course_1, faculty=self.faculty)
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 3,
                     "lecture_quality": 3,
                     "overall_quality": 3,
                     "oral_written_tests_helpful": 3,
                     "learned_much_info": 3}
        response = client.post('/rank/', data=form_data)
        response = client.get('/display/')

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "display.html")

        self.assertEqual(query_set[0].usefulness, 3)
        self.assertEqual(query_set[0].lecture_quality, 3)
        self.assertEqual(query_set[0].overall_quality, 3)
        self.assertEqual(query_set[0].oral_written_tests_helpful, 3)
        self.assertEqual(query_set[0].learned_much_info, 3)

        response = client.post('/login/', {'username':'test2', 'password':'testpassword2'})

        course_pair = Course_Faculty_Table.objects.get(course=self.course_1, faculty=self.faculty)
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 5,
                     "lecture_quality": 5,
                     "overall_quality": 5,
                     "oral_written_tests_helpful": 5,
                     "learned_much_info": 5}
        response = client.post('/rank/', data=form_data)
        response = client.get('/display/')

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "display.html")

        self.assertEqual(query_set[0].usefulness, 4)
        self.assertEqual(query_set[0].lecture_quality, 4)
        self.assertEqual(query_set[0].overall_quality, 4)
        self.assertEqual(query_set[0].oral_written_tests_helpful, 4)
        self.assertEqual(query_set[0].learned_much_info, 4)

