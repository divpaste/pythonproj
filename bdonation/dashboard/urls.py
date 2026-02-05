from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage, name="homepage"),
    path("inbox", views.InboxPage, name="inbox"),
    path("request", views.send_request, name="send_request"),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path("send_manual_request/", views.send_manual_request, name="send_manual_request")
]