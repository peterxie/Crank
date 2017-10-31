from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


#begin Tony-Frank pair insert
class Course_Listing_Table(models.Model):
    coursenumber=models.CharField(max_length=10)
    coursetitle=models.CharField(max_length=128)

class Faculty_Table(models.Model):
    facultyname = models.CharField(max_length=128)

class Course_Faculty_Table(models.Model):
    course = models.ForeignKey(Course_Listing_Table)
    faculty = models.ForeignKey(Faculty_Table)

#class Student_Course_Rating_Table(models.Model):
#    uni = models.ForeignKey(User, null=True)
#    class_id = models.ForeignKey(Course_Faculty_Table)
#    student_course = models.IntegerField(primary_key=True)

class Rating_id(models.Model):
    id = models.AutoField(primary_key=True)
    uni = models.ForeignKey(User)
    course = models.ForeignKey(Course_Faculty_Table)
    class Meta:
        unique_together = (("uni", "course"))
    # #old# unique_id = models.ForeignKey(Student_Course_Rating_Table)
    usefulness = models.IntegerField()
    lecture_quality = models.IntegerField()
    overall_quality = models.IntegerField()
    oral_written_tests_helpful = models.IntegerField()
    learned_much_info = models.IntegerField()

#end Tony-Frank pair insert

class Course(models.Model):
    course_number = models.CharField(max_length = 30)
    @classmethod
    def create(cls, course_number):
        course_number = cls(course_number=course_number)
        # do something with the book
        return course_number


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
