from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from users.models import User, DonationRequest
from users.forms import DonationRequestForm
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

@login_required(login_url = 'login')
def HomePage(request):
    user = request.user 
    form = DonationRequestForm() if request.user.is_authenticated and request.user.role == "R" else None

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

    return render(request, "homepage.html", {"donors_json": donors_json, "donors": donors, "has_filled": has_filled, "requests" : requests, "form": form})

@login_required(login_url='login')
def InboxPage(request):
    user = request.user

    tab = request.GET.get("tab", "all")

    requests = DonationRequest.objects.filter(donor=user)

    if tab == "pending":
        requests = requests.filter(status="Pending")

    elif tab == "accepted":
        requests = requests.filter(status="Accepted")

    elif tab == "rejected":
        requests = requests.filter(status="Rejected")

    requests = requests.order_by("-created_at")

    context = {
        "requests": requests,
        "active_tab": tab
    }

    return render(request, "inbox.html", context)

@login_required(login_url = 'login')
def send_request(request):
    if request.method != "POST":
        return redirect("homepage")

    user = request.user

    if user.role != "R":
        return redirect("homepage")
    
    existing_request = DonationRequest.objects.filter(receiver=user).exists()
    if existing_request:
        messages.warning(request, "You already have an active blood donation request.")
        return redirect("homepage")

    form = DonationRequestForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid request data. Please check the form.")
        print(form.errors)
        return redirect("homepage")
    
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

    requested_bg = request.user.bgroup
    contact = form.cleaned_data["contact"]

    compatible_donor_groups = [
        donor_group
        for donor_group, receivers in BLOOD_COMPATIBILITY.items()
        if requested_bg in receivers
    ]

    compatible_donors = User.objects.filter(
        role="D",
        bgroup__in=compatible_donor_groups
    )

    if not compatible_donors.exists():
        messages.info(request, "No compatible donors available at the moment.")
        return redirect("homepage")

    for donor in compatible_donors:
        DonationRequest.objects.get_or_create(
            donor=donor,
            receiver=user,
            defaults={
                "requested_bg": requested_bg,
                "contact": contact,
            }
        )

    messages.success(request, "Blood donation request sent successfully!")
    return redirect("homepage")

@login_required(login_url='login')
def accept_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id, donor=request.user)

    donation_request.status = 'Accepted'
    donation_request.save()

    return redirect('inbox')

@login_required(login_url='login')
def reject_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id, donor=request.user)

    donation_request.status = 'Rejected'
    donation_request.save()

    return redirect('inbox')
        
@require_POST
def send_manual_request(request):
    if not request.user.is_authenticated or request.user.role != "R":
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    existing_request = DonationRequest.objects.filter(receiver=request.user).exists()
    if existing_request:
        return JsonResponse({"error": "You already have an active blood donation request."}, status=400)
    
    try:
        data = json.loads(request.body)
        donor_ids = data.get("donor_ids", [])
        requested_bg = request.user.bgroup
        contact = data.get("contact")

    except Exception:
        return JsonResponse({"error": "Invalid data"}, status=400)
    
    if not donor_ids or not isinstance(donor_ids, list):
        return JsonResponse({"error": "No donors selected"}, status=400)
    
    donors = User.objects.filter(id__in=donor_ids, role="D")
    if not donors.exists():
        return JsonResponse({"error": "No valid donors found"}, status=400)

    created_count = 0
    for donor in donors:
        obj, created = DonationRequest.objects.get_or_create(
            donor=donor,
            receiver=request.user,
            defaults={
                "requested_bg": requested_bg,
                "contact": contact
            }
        )
        if created:
            created_count += 1

    if created_count == 0:
        return JsonResponse({"error": "Requests already exist for selected donors"}, status=400)
    
    return JsonResponse({"message": f"{created_count} donation request(s) sent successfully."})

@login_required(login_url='login')
def ReceiverInboxPage(request):
    user = request.user

    requests = DonationRequest.objects.filter(receiver=user)

    context = {
        "requests": requests
    }

    return render(request, "receiver_inbox.html", context)


