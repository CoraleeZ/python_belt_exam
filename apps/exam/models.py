from __future__ import unicode_literals
from django.db import models
from datetime import datetime,timedelta
import re

email_regex=re.compile(r'^[a-zA-Z0_9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# name_regex=re.compile(r'^[a-zA-Z]')
# pw_regex=re.compile('\d.*[A-Z]|[A-Z].*\d')

#regex validation
class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
      
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fn']) < 2:
            errors["fn"] = "First name should be at least 2 characters"
        if len(postData['ln']) < 2:
            errors["ln"] = "Last name should be at least 2 characters"
        if not email_regex.match(postData['em']):
            errors['em']='Email is not valid'
        if users.objects.filter(email=postData['em']):
            errors['em']='This email address already existed'
        if len(postData['pw']) < 8:
            errors["pw"] = "Password should be at least 8 characters"
        if postData['cpw']!=postData['pw']:
            errors['cpw']='Password does not match'
        return errors


class TripsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
      
        # add keys and values to errors dictionary for each invalid field
        if len(postData['destination']) < 3:
            errors["destination"] = "Destination should be at least 3 characters"

        #####start date    
        if len(postData['start']) < 1:
            errors["start"] = "Start date should not be empty"

        valuest = postData['start']
        if datetime.now()>datetime.strptime(valuest, '%m/%d/%Y'):
            errors['start']="Start date should not be early than today"
        #####end date
        if len(postData['end']) < 1:
            errors["end"] = "End date should not be empty"
        valueed = postData['end']
        if datetime.strptime(valuest, '%m/%d/%Y')>datetime.strptime(valueed, '%m/%d/%Y'):
            errors['end']="End date should not be early than start date"


        if len(postData['plan']) < 3:
            errors["plan"] = "Plan should be at least 3 characters"
        return errors



class users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #mytrip = user_create
    #jointrip = user_join
    objects = UsersManager() 

class trips(models.Model):
    destination=models.CharField(max_length=255)
    start_date=models.CharField(max_length=255)
    end_date=models.CharField(max_length=255)
    plan=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user_create=models.ForeignKey(users,related_name='mytrip')
    user_join=models.ManyToManyField(users,related_name='jointrip')
    objects = TripsManager()




# Create your models here.
