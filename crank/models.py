from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Course_Listing_Table(models.Model):
    coursenumber=models.CharField(max_length=10, primary_key=True)
    coursetitle=models.CharField(max_length=128)

    def __str__(self):
        return u'{0}'.format(self.coursenumber)

class Faculty_Table(models.Model):
    facultyname = models.CharField(max_length=128, primary_key=True)
    
    def __str__(self):
        return u'{0}'.format(self.facultyname)

class Course_Faculty_Table(models.Model):
    course = models.ForeignKey(Course_Listing_Table)
    faculty = models.ForeignKey(Faculty_Table)

    class Meta:
        unique_together = (("course", "faculty"))

    def __str__(self):
      return u'{0}/{1}'.format(self.course, self.faculty)

class Rating_id(models.Model):
    id = models.AutoField(primary_key=True)
    uni = models.ForeignKey(User)
    course = models.ForeignKey(Course_Faculty_Table)

    usefulness = models.IntegerField()
    lecture_quality = models.IntegerField()
    overall_quality = models.IntegerField()
    oral_written_tests_helpful = models.IntegerField()
    learned_much_info = models.IntegerField()

    class Meta:
        unique_together = (("uni", "course"))

class Rating_Average(models.Model):
    course = models.CharField(max_length=128, primary_key=True)

    usefulness = models.FloatField()
    lecture_quality = models.FloatField()
    overall_quality = models.FloatField()
    oral_written_tests_helpful = models.FloatField()
    learned_much_info = models.FloatField()
