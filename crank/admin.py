from django.contrib import admin
from .models import Course_Listing_Table, Faculty_Table, Course_Faculty_Table, Student_Course_Rating_Table, Course_Rating_Table, Greeting, Profile 

# Register your models here.
admin.site.register(Course_Listing_Table)
admin.site.register(Faculty_Table)
admin.site.register(Course_Faculty_Table)
admin.site.register(Student_Course_Rating_Table)
admin.site.register(Course_Rating_Table)
admin.site.register(Greeting)
admin.site.register(Profile)

