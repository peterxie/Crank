from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class User(models.Model):
    name = models.CharField(max_length = 30, primary_key=True)
    userName = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
