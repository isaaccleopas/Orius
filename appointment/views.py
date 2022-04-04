from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

# Create your views here.


# For Patient Profile
    

class EditPatientProfileView(UpdateView):
    model = User
    form_class = PatientProfileUpdateForm
    context_object_name = 'patient'
    template_name = 'accounts/patient/edit-profile.html'
    success_url = reverse_lazy('accounts:patient-profile-update')

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


class TakeAppointmentView(CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('appointment:home')

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


class EditTherapistProfileView(UpdateView):
    model = User
    form_class = TherapistProfileUpdateForm
    context_object_name = 'therapist'
    template_name = 'accounts/therapist/edit-profile.html'
    success_url = reverse_lazy('accounts:therapist-profile-update')

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


class AppointmentCreateView(CreateView):
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('appointment:therapist-appointment')

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


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_therapist)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


class PatientListView(ListView):
    model = TakeAppointment
    context_object_name = 'patients'
    template_name = "appointment/patient_list.html"

    def get_queryset(self):
        return self.model.objects.filter(appointment__user_id=self.request.user.id).order_by('-id')


class PatientDeleteView(DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('appointment:patient-list')


class AppointmentDeleteView(DeleteView):

    #    For Delete any Appointment created by Therapist
    model = Appointment
    success_url = reverse_lazy('appointment:therapist-appointment')


#    For both Profile


class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "home.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


class SearchView(ListView):
    paginate_by = 6
    model = Appointment
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return self.model.objects.filter()

# class PreviousSessionsView(ListView):
#     model = TakeAppointment
#     context_object_name = 'patients'
#     template_name = "appointment/patient_list.html"

#     def get_queryset(self):
#         return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')

class AppointmentStatusView(UpdateView):

    model = Appointment
    template_name = "appointment/appointment_status.html"
    context_object_name = 'appointment'
    form_class = AppoinmentStatusUpdateForm

    # def get(self, request, *args, **kwargs):
    #     allOrders = Order.objects.all()
    #     args = {"allOrders": allOrders}
    #     return render(request, self.template_name, args)

    # def post(self, request):
    #     orderId = self.request.GET.get("order_id")
    #     statusAccept = self.request.GET.get("acceptButton")
    #     statusReject = self.request.GET.get("rejectButton")

    #     if statusAccept:
    #         try:
    #             orderDecision = OrderRequest(
    #                 order_id=orderId,
    #                 order_status=statusAccept,
    #             )
    #             orderDecision.save()
    #             return redirect("orderDecision")
    #         except Exception as e:
    #             return HttpResponse("failed{}".format(e))

    #     if statusReject:
    #         remove = Order.objects.get(pk=statusReject.id)
    #         delete(remove)