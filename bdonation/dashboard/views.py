from django.shortcuts import render
from django.http import HttpResponse
from users.models import Donor
import json
from django.contrib.auth.decorators import user_passes_test

def HomePage(request):
    has_filled = False

    donors = Donor.objects.all()
    donors_list = []

    if request.user.is_authenticated:
        has_filled = Donor.objects.filter(user=request.user).exists()

    for d in donors:
        donors_list.append({
            "name": d.name,
            "bgroup": d.bgroup,
            "contact": d.contact,
            "latitude": float(d.latitude),
            "longitude": float(d.longitude),
        })

    donors_json = json.dumps(donors_list)

    return render(request, "homepage.html", {"donors_json": donors_json, "has_filled": has_filled})

@user_passes_test(lambda u: u.is_superuser, login_url="login")
def RequestsPage(request):
    donors = Donor.objects.all()
    donors_list = []

    for d in donors:
        donors_list.append({
            "name": d.name,
            "bgroup": d.bgroup,
            "contact": d.contact,
            "age": d.age,
            "latitude": float(d.latitude),
            "longitude": float(d.longitude),
            "height": d.height,
            "weight": d.weight,
            "status": d.status,
            "previous_donor": d.previous_donor
        })

    donors_json = json.dumps(donors_list)

    return render(request, "requests.html", {"donors_json": donors_json})