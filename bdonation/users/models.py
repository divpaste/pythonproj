from django.db import models
from django.contrib.auth.models import AbstractUser, User

class UserProfile(AbstractUser):
    role_choices = [("R" , "R"), ("D", "D")]
    role = models.CharField(max_length=1, choices=role_choices)

class Donor(models.Model):
    user  = models.OneToOneField(UserProfile, on_delete=models.CASCADE)    

    bgroup_choices = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    status_choices = [
        ("P", "Pending"),
        ("A", "Accepted"),
        ("R", "Rejected")
    ]

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    bgroup = models.CharField(max_length=3, choices=bgroup_choices)
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    med_history = models.TextField(blank=True)
    previous_donor = models.BooleanField()
    contact = models.CharField(max_length=10)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    status = models.CharField(max_length=1, choices=status_choices, default="P")