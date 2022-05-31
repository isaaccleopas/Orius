from django import forms
from .models import Appointment, TakeAppointment


class CreateAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        # self.fields['full_name'].label = "Full Name"
        self.fields['start_time'].label = "Start Time"
        self.fields['end_time'].label = "End Time"
        # self.fields['message'].label = "Message"

        # self.fields['full_name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Full Name',
        #     }
        # )
        self.fields['start_time'].widget.attrs.update(
            {
                'placeholder': 'Ex : 9 AM',
            }
        )
        self.fields['end_time'].widget.attrs.update(
            {
                'placeholder': 'Ex: 5 PM',
            }
        )
        
        # self.fields['message'].widget.attrs.update(
        #     {
        #         'placeholder': 'Write a short message',
        #     }
        # )
        
    class Meta:
        model = Appointment
        fields = [ 'start_time', 'end_time']

    def is_valid(self):
        valid = super(CreateAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(CreateAppointmentForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment


class TakeAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TakeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['appointment'].label = "Choose Your Therapist"
        # self.fields['full_name'].label = "Full Name"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['the_challenge'].label = "The Challenge"
        # self.fields['gender'].required = True
        # self.fields['age'].label = "Age"
        # self.fields['location'].label = "Location"
        # self.fields['email'].label = "Email"

        self.fields['appointment'].queryset = Appointment.objects.exclude(status="APPROVED")
        # self.fields['appointment'].widget = forms.HiddenInput()

        self.fields['appointment'].widget.attrs.update(
            {
                'placeholder': 'Choose Your Therapist',
            }
        )

        # self.fields['full_name'].widget.attrs.update(
        #     {
        #         'placeholder': 'Write Your Name',
        #         # 'disabled': True,
        #         # 'value': self.request.user.first_name + " " + self.request.user.last_name
        #     }
        # )

        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )

        self.fields['the_challenge'].widget.attrs.update(
            {
                'placeholder': 'Write a short message',
            }
        )
        # self.fields['age'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Age',
        #     }
        # )
        # self.fields['location'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Location',
        #     }
        # )
        # self.fields['email'].widget.attrs.update(
        #     {
        #         'placeholder': 'Enter Email',
        #     }
        # )
    class Meta:
        model = TakeAppointment
        fields = ['appointment', 'phone_number', 'the_challenge']

    def is_valid(self):
        valid = super(TakeAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(TakeAppointmentForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment

class AppoinmentStatusUpdateForm(forms.ModelForm):
    status = forms.CharField(initial="APPROVED")
    # widget=forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super(AppoinmentStatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = "APPROVED"
    
    class Meta:
        model = Appointment
        fields = ['status']