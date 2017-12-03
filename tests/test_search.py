from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client

from crank.views import *
from crank.models import *

USEFULNESS_C = 5
LECTURE_QUALITY_C = 4 
OVERALL_C = 3
ORAL_WRITTEN_C = 2
LEARNED_MUCH_C = 1
FACULTY_PARTIAL_1 = "TEST "
FACULTY_PARTIAL_2 = "FACULTY"
FACULTY_NAME_C = FACULTY_PARTIAL_1 + FACULTY_PARTIAL_2
COURSE_PARTIAL_1 = "COMSW"
COURSE_PARTIAL_2 = "4156"
COURSE_NUMBER_C = COURSE_PARTIAL_1 + COURSE_PARTIAL_2

class TestSearch(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='test', email='test@columbia.edu', password='testpassword')

        self.course = Course_Listing_Table.objects.create(coursenumber=COURSE_NUMBER_C, 
                                                          coursetitle="Advanced Software Engineering")
        self.faculty = Faculty_Table.objects.create(facultyname=FACULTY_NAME_C)
        self.course_faculty = Course_Faculty_Table.objects.create(course=self.course, faculty=self.faculty) 
        self.rating_average = Rating_Average.objects.create(course_faculty=self.course_faculty,
                                                            usefulness=USEFULNESS_C,
                                                            lecture_quality=LECTURE_QUALITY_C,
                                                            overall_quality=OVERALL_C,
                                                            oral_written_tests_helpful=ORAL_WRITTEN_C,
                                                            learned_much_info=LEARNED_MUCH_C,
                                                            rating_count=1)

    def testSearch(self):
        client = Client()

        form_data = {"course": "",
                     "faculty": ""}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testSearchCourse(self):
        client = Client()

        form_data = {"course": self.course.coursenumber,
                     "faculty": ""}
        response = client.get('/search/', data=form_data)
        
        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testSearchFaculty(self):
        client = Client()

        form_data = {"course": "",
                     "faculty": self.faculty.facultyname}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testSearchFail(self):
        client = Client()

        form_data = {"course": "",
                     "faculty": "!"}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(len(query_set), 0)

    def testSearchFacultyPartial1(self):
        client = Client()

        form_data = {"course": "",
                     "faculty": FACULTY_PARTIAL_1}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testSearchFacultyPartial2(self):
        client = Client()

        form_data = {"course": "",
                     "faculty": FACULTY_PARTIAL_2}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testSearchCoursePartial1(self):
        client = Client()

        form_data = {"course": COURSE_PARTIAL_1,
                     "faculty": ""}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testSearchCoursePartial2(self):
        client = Client()

        form_data = {"course": COURSE_PARTIAL_2,
                     "faculty": ""}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)

    def testBothPartial(self):
        client = Client()

        form_data = {"course": COURSE_PARTIAL_2,
                     "faculty": FACULTY_PARTIAL_1}
        response = client.get('/search/', data=form_data)

        query_set = response.context["rating_average"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertEqual(query_set[0], self.rating_average)


