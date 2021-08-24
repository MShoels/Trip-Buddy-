from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['fname'])<2: 
            errors['fname'] = "First Name should be at least 2 characters."
        if len(postData['lname'])<2: 
            errors['lname'] = "Last Name should be at least 2 characters."
        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['checkpassword']:
            errors['nomatch'] = "Passwords must match."
        if not EMAIL_REGEX.match(postData['email']):
            errors['format'] = "Invalid email address."
        if len(User.objects.filter(email=postData['email']))>0:
            errors['inuse'] = "Email in use."
        return errors

    def login_validator(self, postData):
        errors={}
        email = postData['email']
        user=User.objects.filter(email=email)
        print(user)
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailformat'] = "Invalid login."
        if len(user) < 1:
            errors['emailnot'] = "Invalid login."
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors={}
        print(postData['start_date'])
        print(postData['end_date'])
        if len(postData['destination']) < 3:
            errors["destination"]= "Destination must be at least 3 characters!"
        if len(postData['plan']) < 3:
            errors["plan"]= "Plan must be at least 3 characters!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    password =models.CharField(max_length=255)
    created_at =models.DateField(auto_now_add=True)
    updated_at =models.DateField(auto_now=True)
    objects =UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    plan = models.TextField()
    planner = models.ForeignKey(User, related_name='my_trips', on_delete=models.CASCADE)
    guest = models.ManyToManyField(User, related_name='trips')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects =TripManager()