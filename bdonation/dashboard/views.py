from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

def HomePage(request):
    return render(request, "homepage.html")