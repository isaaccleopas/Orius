from django.urls import path
from appointment.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'appointment'

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('therapist/appointment/create', AppointmentCreateView.as_view(), name='therapist-appointment-create'),
    path('therapist/appointment/', AppointmentListView.as_view(), name='therapist-appointment'),
    path('<pk>/delete/', AppointmentDeleteView.as_view(), name='delete-appointment'),
    path('<pk>/patient/delete', PatientDeleteView.as_view(), name='delete-patient'),
    path('patient-take-appointment/<pk>', TakeAppointmentView.as_view(), name='take-appointment'),
    path('search/', SearchView.as_view(), name='search'),
    path('patient/', PatientListView.as_view(), name='patient-list'),
    path('<pk>/appointment-status/', AppointmentStatusView.as_view(), name='appointment-status'),
    path('session/', PreviousSessionsView.as_view(), name='session-list'),
    path('patient/therapists/', TherapistListView.as_view(), name='therapist-list'),

    # path('patients/<int:appointment_id>', PatientPerAppointmentView.as_view(), name='patient-list'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)