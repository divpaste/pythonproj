from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DonationRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username','bgroup')

admin.site.register(DonationRequest)