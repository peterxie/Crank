from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
This Profile model is used to track email verification of a user.
First set User and Profile in a 1 to 1 relation.
Then set default value of email_confirmed to false because only
after verification will this field be set true.
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

#A callback executes after post_save on a user object. If a 
#user object is created for the first time we will create a new
#profile in tandem.
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

"""
This class is an instantiation of Course_Listing_Table and the
__str__ allows us to print only the coursenumber when invoked.
"""
class Course_Listing_Table(models.Model):
    coursenumber=models.CharField(max_length=12, primary_key=True)
    coursetitle=models.CharField(max_length=128)

    def __str__(self):
        return u'{0}'.format(self.coursenumber)

"""
This class is an instantiation of Faculty_Table and the
__str__ allows us to print only the Faculty name when invoked. 
"""
class Faculty_Table(models.Model):
    facultyname = models.CharField(max_length=128, primary_key=True)
    
    def __str__(self):
        return u'{0}'.format(self.facultyname)

"""
This class is an instantiation of Faculty_Table and the
__str__ allows us to print the professor and course recursively when invoked.
This table references faculty and courses so they are unique so that we don't
have multiple professors mapped to one course.  
"""
class Course_Faculty_Table(models.Model):
    course = models.ForeignKey(Course_Listing_Table, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty_Table, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("course", "faculty"))

    def __str__(self):
      return u'{0}/{1}'.format(self.course, self.faculty)

"""
This class is an instantiation of a Rating. This links all the rating fields
to a rating and matches the faculty and course. This table references user 
and course_faculty so they are unique so that we don't have multiple ratings 
from one user to one class pairing.  
"""
class Rating_id(models.Model):
    id = models.AutoField(primary_key=True)
    uni = models.ForeignKey(User, on_delete=models.CASCADE)
    course_faculty = models.ForeignKey(Course_Faculty_Table, on_delete=models.CASCADE)

    usefulness = models.IntegerField()
    lecture_quality = models.IntegerField()
    overall_quality = models.IntegerField()
    oral_written_tests_helpful = models.IntegerField()
    learned_much_info = models.IntegerField()
    comments = models.CharField(max_length=2000)

    class Meta:
        unique_together = (("uni", "course_faculty"))

"""
This class is an instantiation of the average Rating. This will be an aggregate of
all the ratings submitted.
"""
class Rating_Average(models.Model):
    course_faculty = models.ForeignKey(Course_Faculty_Table, on_delete=models.CASCADE)

    usefulness = models.FloatField()
    lecture_quality = models.FloatField()
    overall_quality = models.FloatField()
    oral_written_tests_helpful = models.FloatField()
    learned_much_info = models.FloatField()
    rating_count = models.IntegerField()
