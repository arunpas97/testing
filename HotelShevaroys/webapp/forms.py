from django import forms

from webapp.models import *

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'