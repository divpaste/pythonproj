from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    role_choices = [("R" , "Reciever"), ("D", "Donor")]

    bgroup_choices = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    full_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    bgroup = models.CharField(max_length=3, choices=bgroup_choices, null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    med_history = models.TextField(blank=True)
    previous_donor = models.BooleanField(default=False)
    contact = models.CharField(max_length=10, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    role = models.CharField(max_length=1, choices=role_choices, default="R")

class DonationRequest(models.Model):
    status_choices = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    bgroup_choices = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="sent_requests",on_delete=models.CASCADE)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="received_requests",on_delete=models.CASCADE)

    requested_bg = models.CharField(max_length=3,choices=bgroup_choices)
    contact = models.CharField(max_length=10)
    status = models.CharField(max_length=10,choices=status_choices,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)