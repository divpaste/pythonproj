from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from users.models import User, DonationRequest
import json
from django.contrib.auth.decorators import user_passes_test, login_required

@login_required(login_url = 'login')
def HomePage(request):
    user = request.user 

    donors = User.objects.filter(role="D")
    donors_list = []

    requests = DonationRequest.objects.filter(receiver=request.user)

    has_filled = True if user.role == "D" else False

    for d in donors:
        donors_list.append({
            "id": d.id,
            "full_name": d.full_name,
            "bgroup": d.bgroup,
            "contact": d.contact,
            "latitude": float(d.latitude or 0),
            "longitude": float(d.longitude or 0),
        })

    donors_json = json.dumps(donors_list)

    return render(request, "homepage.html", {"donors_json": donors_json, "donors": donors, "has_filled": has_filled, "requests" : requests})

@login_required(login_url = 'login')
def InboxPage(request):
    user = request.user

    if user.role != "D":
        return redirect("homepage")
    
    requests = DonationRequest.objects.filter(donor=user)

    return render(request, "inbox.html", {"requests" : requests})

@login_required(login_url = 'login')
def send_request(request):
    BLOOD_COMPATIBILITY = {
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'O-': ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'],
    'A+': ['A+', 'AB+'],
    'A-': ['A+', 'A-', 'AB+', 'AB-'],
    'B+': ['B+', 'AB+'],
    'B-': ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'],
    'AB-': ['AB+', 'AB-'],
    }

    user = request.user

    if user.role != "R":
        return redirect("homepage")
    
    receiver_group = user.bgroup

    compatible_donor_groups = [
        donor_group
        for donor_group, receivers in BLOOD_COMPATIBILITY.items()
        if receiver_group in receivers
    ]

    compatible_donors = User.objects.filter(
        role="D",
        bgroup__in=compatible_donor_groups
    )

    for donor in compatible_donors:
        DonationRequest.objects.get_or_create(
            donor=donor,
            receiver=user
        )

    return redirect("homepage")

@login_required(login_url = 'login')
def delete_request(request, donor_id):

    donation = get_object_or_404(
        DonationRequest,
        donor_id=donor_id,
        receiver=request.user
    )

    donation.delete()
    return redirect("homepage")
        