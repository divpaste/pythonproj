from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegistrationForm, BloodDonationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import BloodDonationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings 

def LoginPage(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"User {user} successfully logged in")
            return redirect('homepage')
        
    return render(request, "login.html", {"form": form})

def LogOut(request):
    logout(request)
    return redirect('login')

def RegisterPage(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f"User {user} successfully created")
            return redirect("login")
    
    return render(request, "register.html", {"form": form})

@login_required(login_url = 'login')
def DonatePage(request):
    form = BloodDonationForm()

    if request.method == 'POST':
        form = BloodDonationForm(request.POST, instance=request.user)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.role = "D"
            donor.save()
            messages.success(request, "Donation info saved! 🎉")
            return redirect('homepage')  
        else:
            print("Error: ")
            messages.error(request, "Donation not saved! 🎉")
            print(form.errors)

    return render(request, "form.html", {"form": form, "API_KEY": settings.MAP_API_KEY})