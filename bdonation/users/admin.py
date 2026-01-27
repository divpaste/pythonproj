from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    pass