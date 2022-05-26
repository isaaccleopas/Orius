from django.db import models
from django.urls import reverse
from django.utils import timezone
from accounts.models import User

# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    status = models.TextField(default='PENDING')
    
    def __str__(self):
        desc = '{} {}'.format(self.user.first_name, self.user.last_name)
        return desc

    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})
GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))

class TakeAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.CharField(max_length=3,null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    location = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=100,null=True)
    the_challenge = models.TextField(max_length=500,null=True)
    phone_number = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)
    status = models.TextField(default='PENDING')

    def __str__(self):
        return self.full_name