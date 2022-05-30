from django.urls import path
from .views import *
from appointment.views import *
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('patient/register', RegisterPatientView.as_view(), name='patient-register'),
    path('patient/profile/update/', EditPatientProfileView.as_view(), name='patient-profile-update'),
    path('therapist/register', RegisterTherapistView.as_view(), name='therapist-register'),
    path('therapist/profile/update/', EditTherapistProfileView.as_view(), name='therapist-profile-update'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('patient-password/', auth_views.PasswordChangeView.as_view(
            template_name='commons/patient-password.html',
            success_url = 'patient-password'), name='patient-password'),
    # path('', TherapistPassword.as_view(), name='therapist-password'),
]