from __future__ import unicode_literals

from django.contrib import messages
from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_login(self, post):
        user = User.objects.filter(email=post['email']).first()
        if user and bcrypt.checkpw(post['password'].encode(), user.password.encode()):
            return { 'status': True, 'user': user}
        else:
            return { 'status': False, 'error': 'Invalid credentials' }



    def validate_registration(self, post):
        #step 1: validate the form data
         errors = []
         if post['name'] == '':
             errors.append('Name cannot be blank')
         if post['alias'] == '':
             errors.append('Alias cannot be blank')
         if post['email'] == '':
             errors.append('Email cannot be blank')
         user = User.objects.filter(email=post['email']).first()
         if user:
             errors.append('Email already in use')
         if len(post['password']) < 8:
             errors.append('password must be at least eight characters')
         if len(post['dob']) < 1:
            errors.append('Date of birth cannot be blank.')
         elif post['password'] != post['password_confirmation']:
             errors.append('Passwords do not match')
        #step2: if invalid create error messages
         if not errors:
             user = User.objects.create(
                name=post['name'],
                alias=post['alias'],
                email=post['email'],
                password=bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt(10)),
                dob=post['dob']
             )
             return { 'status': True, 'user' : user }
         else:
             return { 'status': False, 'errors': errors }
        #step3: if valid create the user and the session



class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    friends = models.ManyToManyField("self")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
