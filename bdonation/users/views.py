from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

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
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f"User {user} successfully created")
            return redirect("login")
    
    return render(request, "register.html", {"form": form})