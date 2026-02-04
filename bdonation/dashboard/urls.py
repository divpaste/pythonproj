from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage, name="homepage"),
    path("inbox", views.InboxPage, name="inbox"),
    path("request", views.send_request, name="send_request")
]