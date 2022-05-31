from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from accounts.models import User
from .decorators import user_is_patient, user_is_therapist
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from django.views.generic.edit import DeleteView, UpdateView
from accounts.forms import PatientProfileUpdateForm, TherapistProfileUpdateForm
from .forms import CreateAppointmentForm, TakeAppointmentForm
from .models import Appointment, TakeAppointment
from appointment.forms import AppoinmentStatusUpdateForm

from django.views import View

# Create your views here.


# For Patient Profile
    

class EditPatientProfileView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = PatientProfileUpdateForm
    context_object_name = 'patient'
    template_name = 'accounts/patient/edit-profile.html'
    success_url = reverse_lazy('accounts:patient-profile-update')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "patient"

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_patient)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")

        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj


class TakeAppointmentView(UserPassesTestMixin, CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('appointment:session-list')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "patient"

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'patient':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TakeAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(TakeAppointmentView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs        


#    For Therapist Profile


class EditTherapistProfileView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = TherapistProfileUpdateForm
    context_object_name = 'therapist'
    template_name = 'accounts/therapist/edit-profile.html'
    success_url = reverse_lazy('accounts:therapist-profile-update')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_therapist)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")

        # context = self.get_context_data(object=self.object)

        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Therapist doesn't exists")
        return obj


class AppointmentCreateView(UserPassesTestMixin, CreateView):
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('appointment:therapist-appointment')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'therapist':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AppointmentListView(UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_therapist)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).exclude(status="APPROVED").order_by('-id')


class PatientListView(UserPassesTestMixin, ListView):
    model = TakeAppointment
    context_object_name = 'patients'
    template_name = "appointment/patient_list.html"

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"

    def get_queryset(self):
        return self.model.objects.filter(appointment__user_id=self.request.user.id).order_by('-id')


class PatientDeleteView(UserPassesTestMixin, DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('appointment:patient-list')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"


class AppointmentDeleteView(UserPassesTestMixin, DeleteView):

    #    For Delete any Appointment created by Therapist
    model = Appointment
    success_url = reverse_lazy('appointment:therapist-appointment')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"

#    For both Profile


class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.exclude(status="APPROVED").order_by('-id')


class SearchView(ListView):
    paginate_by = 6
    model = Appointment
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return self.model.objects.filter()

class PreviousSessionsView(UserPassesTestMixin, ListView):
    model = TakeAppointment
    context_object_name = 'sessions'
    template_name = "appointment/session_list.html"
    
    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "patient"

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['appointments'] = Appointment.objects.filter(status="PENDING")
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')

class AppointmentStatusView(UserPassesTestMixin, UpdateView):
    model = TakeAppointment
    template_name = "appointment/appointment_status.html"
    context_object_name = 'appointment'
    form_class = AppoinmentStatusUpdateForm
    success_url = reverse_lazy('appointment:patient-list')

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "therapist"

    def get_initial(self):
        return {'status': "APPROVED"}

    def post(self, request, *args, **kwargs):
        
        
        status = request.POST['status']
        pk = kwargs['pk']
        take_appointment_model = self.model.objects.get(pk=pk)

        # Change the status field in the parent (appointment) model to approved (what was passed)
        take_appointment_model.appointment.status = status
        take_appointment_model.appointment.save()


        # Change the status of the other TakeAppointments to cancelled
        # get all the other takeappointments
        appointment_id_we_are_interested_in = take_appointment_model.appointment.id
        all_the_other_take_appointments = self.model.objects.filter(appointment_id=appointment_id_we_are_interested_in).exclude(id=take_appointment_model.id)
        
        # update their status to cancelled
        all_the_other_take_appointments.update(status="CANCELLED")

        # # save
        # all_the_other_take_appointments.save()
        
        # print(take_appointment_model.appointment.status)
        return super().post(request, args, kwargs)

class TherapistListView(UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'therapists'
    template_name = "appointment/therapist_list.html"

    login_url="/"

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.role == "patient"

    def get_queryset(self):
        return self.model.objects.filter(role='therapist')