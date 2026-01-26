from django.db import models
from django.contrib.auth.models import User

# User Model
class UserProfile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)

    gender_choices = (
    ('M', 'Male'),
    ('F', 'Female')
    )
    role_choices = (
    ('D', 'Donor'),
    ('R', 'Receiver')
    )
    bgroup_choices = (
    ('O+', 'O Positive'),
    ('O-', 'O Negative'),
    ('A+', 'A Positive'),
    ('A-', 'A Negative'),
    ('B+', 'B Positive'),
    ('B-', 'B Negative'),
    ('AB+', 'AB Positive'),
    ('AB-', 'AB Negative')
    )
    gender = models.CharField(max_length=1, choices=gender_choices)
    dob = models.DateField()
    role = models.CharField(max_length=1, choices=role_choices)
    contact = models.CharField(max_length=10, unique=True)
    bgroup = models.CharField(max_length=3, choices=bgroup_choices)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)