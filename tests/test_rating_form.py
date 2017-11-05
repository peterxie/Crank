from django.test import TestCase
from crank.forms import *

class TestRatingForm(TestCase):

    def setUp(self):
        self.course = Course_Listing_Table.objects.create(coursenumber="COMSW4156", coursetitle="Advanced Software Engineering")
        self.faculty = Faculty_Table.objects.create(facultyname="TEST FACULTY")
        Course_Faculty_Table.objects.create(course=self.course, faculty=self.faculty) 

    def testValidForm(self):
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 2,
                     "lecture_quality": 1,
                     "overall_quality": 5,
                     "oral_written_tests_helpful": 3,
                     "learned_much_info": 4}

        form = RankForm(form_data)
        self.assertTrue(form.is_valid())

    def testInvalidFormMissingCourseSelection(self):
        form_data = {"course_faculty_pair": "",
                     "usefulness": 2,
                     "lecture_quality": 1,
                     "overall_quality": 1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}

        form = RankForm(form_data)
        self.assertFalse(form.is_valid())

    def testInvalidFormNegativeRating(self):
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 2,
                     "lecture_quality": -1,
                     "overall_quality": 1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}

        form = RankForm(form_data)
        self.assertFalse(form.is_valid())

    def testInvalidFormZeroRating(self):
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 2,
                     "lecture_quality": 0,
                     "overall_quality": 1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}

        form = RankForm(form_data)
        self.assertFalse(form.is_valid())


    def testInvalidFormRatingTooHigh(self):
        form_data = {"course_faculty_pair": 1,
                     "usefulness": 2,
                     "lecture_quality": 6,
                     "overall_quality": 1,
                     "oral_written_tests_helpful": 1,
                     "learned_much_info": 1}

        form = RankForm(form_data)
        self.assertFalse(form.is_valid())


