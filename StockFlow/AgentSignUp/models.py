from email.policy import default
from http.client import LENGTH_REQUIRED
from django.db import models
from django.forms import BooleanField, CharField, IntegerField

# Create your models here.


class Agent(models.Model):
    emp_ID = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=40)
    full_name = models.CharField(max_length=80)
    city = models.CharField(max_length=50)
    Mobile = models.CharField(max_length=10)
    isAgent = models.BooleanField()

    def __str__(self):
        return self.full_name



class Customer(models.Model):
    full_name = models.CharField(max_length=80)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name