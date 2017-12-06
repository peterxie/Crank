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

class TestHistory(TestCase):

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
        self.rating_1 = Rating_id.objects.create(uni=self.user,
                                                 course_faculty=self.course_faculty_1,
                                                 usefulness=USEFULNESS_C,
                                                 lecture_quality=LECTURE_QUALITY_C,
                                                 overall_quality=OVERALL_C,
                                                 oral_written_tests_helpful=ORAL_WRITTEN_C,
                                                 learned_much_info=LEARNED_MUCH_C)

        self.rating_2 = Rating_id.objects.create(uni=self.user,
                                                 course_faculty=self.course_faculty_2,
                                                 usefulness=USEFULNESS_C,
                                                 lecture_quality=LECTURE_QUALITY_C,
                                                 overall_quality=OVERALL_C,
                                                 oral_written_tests_helpful=ORAL_WRITTEN_C,
                                                 learned_much_info=LEARNED_MUCH_C)

        self.rating_avg_1 = Rating_Average.objects.create(course_faculty = self.course_faculty_1,
                                                          usefulness = self.rating_1.usefulness,
                                                          lecture_quality = self.rating_1.lecture_quality,
                                                          overall_quality = self.rating_1.overall_quality,
                                                          oral_written_tests_helpful = self.rating_1.oral_written_tests_helpful,
                                                          learned_much_info = self.rating_1.learned_much_info,
                                                          rating_count = 2)

        self.rating_avg_2 = Rating_Average.objects.create(course_faculty = self.course_faculty_2,
                                                          usefulness = self.rating_2.usefulness,
                                                          lecture_quality = self.rating_2.usefulness,
                                                          overall_quality = self.rating_2.overall_quality,
                                                          oral_written_tests_helpful = self.rating_2.oral_written_tests_helpful,
                                                          learned_much_info = self.rating_2.learned_much_info,
                                                          rating_count = 1)


    def testHistory(self):
        client = Client()

        response = client.post('/login/', {'username':'test', 'password':'testpassword'})
        response = client.get('/history/')

        query_set = response.context["history"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

        #ratings are sorted alphabetically by course number COMSE6156 < COMSW4156
        self.assertEqual(query_set[0], self.rating_2)
        self.assertEqual(query_set[1], self.rating_1)

    def testNoHistory(self):
        client = Client()

        response = client.post('/login/', {'username':'test2', 'password':'testpassword2'})
        response = client.get('/history/')

        query_set = response.context["history"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

        self.assertEqual(len(query_set), 0)

    def testDeleteNoHistory(self):
        client = Client()

        response = client.post('/login/', {'username':'test', 'password':'testpassword'})
        #shouldn't delete anything
        response = client.get('/delete_rank/1038')
        response = client.get('/history/')

        query_set = response.context["history"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

        self.assertEqual(len(query_set), 2)
        #ratings are sorted alphabetically by course number COMSE6156 < COMSW4156
        self.assertEqual(query_set[0], self.rating_2)
        self.assertEqual(query_set[1], self.rating_1)

    def testDeleteLastRanking(self):
        client = Client()

        response = client.post('/login/', {'username':'test', 'password':'testpassword'})
        response = client.get('/delete_rank/' + str(self.rating_2.id) + '/')
        response = client.get('/history/')

        query_set = response.context["history"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

        self.assertEqual(len(query_set), 1)
        self.assertEqual(query_set[0], self.rating_1)
        try:
            Rating_Average.objects.get(id = self.rating_avg_2.id)
            self.fail("Failed to delete rating!")
        except Exception as e:
            pass

    def testDeleteRanking(self):
        client = Client()

        response = client.post('/login/', {'username':'test', 'password':'testpassword'})
        response = client.get('/delete_rank/' + str(self.rating_1.id) + '/')
        response = client.get('/history/')

        query_set = response.context["history"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

        self.assertEqual(len(query_set), 1)
        self.assertEqual(query_set[0], self.rating_2)

        rating_avg = Rating_Average.objects.get(id = self.rating_avg_1.id)

        self.assertEqual(rating_avg.rating_count, 1)
        self.assertEqual(rating_avg.course_faculty, self.course_faculty_1)
        self.assertEqual(rating_avg.usefulness, self.rating_1.usefulness)
        self.assertEqual(rating_avg.lecture_quality, self.rating_1.lecture_quality)
        self.assertEqual(rating_avg.overall_quality, self.rating_1.overall_quality)
        self.assertEqual(rating_avg.oral_written_tests_helpful, self.rating_1.oral_written_tests_helpful)
        self.assertEqual(rating_avg.learned_much_info, self.rating_1.learned_much_info)
