from django.contrib import admin
from .models import Greeting, User

# Register your models here.
admin.site.register(Greeting)
admin.site.register(User)
