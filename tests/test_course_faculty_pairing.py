from django.test import TestCase
from crank.models import Course_Listing_Table, Faculty_Table, Course_Faculty_Table

class RatingTestCase(TestCase):
    def setUp(self):
        course = Course_Listing_Table.objects.create(coursenumber="COMSW4156", coursetitle="Advanced Software Engineering")
        faculty = Faculty_Table.objects.create(facultyname="TEST FACULTY")
        Course_Faculty_Table.objects.create(course=course, faculty=faculty) 

    def test_display_name(self): 
        course = Course_Listing_Table.objects.get(coursenumber="COMSW4156")
        faculty = Faculty_Table.objects.get(facultyname="TEST FACULTY")
        course_faculty_pair = Course_Faculty_Table.objects.get(course=course, faculty=faculty)

        self.assertEqual(str(course), "COMSW4156")
        self.assertEqual(str(faculty), "TEST FACULTY")
        self.assertEqual(str(course_faculty_pair), "COMSW4156/TEST FACULTY")

