from django.db import models
from django.contrib.auth.models import User

# User Model
class UserProfile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)

    role_choices = (
    ('D', 'Donor'),
    ('R', 'Receiver')
    )

    bgroup_choices = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    bgroup = models.CharField(max_length=3, choices=bgroup_choices)
    height = models.IntegerField()
    weight = models.IntegerField()
    med_history = models.TextField()
    recent_travel = models.IntegerField()
    previous_donor = models.IntegerField()
    role = models.CharField(max_length=1, choices=role_choices)
    contact = models.CharField(max_length=10, unique=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)