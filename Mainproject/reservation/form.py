from .models import Identity,Booking
from django import forms
from working.models import Residency
from django.forms.widgets import DateInput


IDI=[ 
        ("Adhar Card", "Adhar Card"),
        ("Passport", "Passport"),
        ("Ration Card", "Ration Card"),
        ("Voter Id", "Voter Id"),
        ("Driving License", "Driving License"),
        ("PAN Card", "PAN Card"),
        ("International Passport", "International Passport"),
        ("National ID", "National ID"),
        ("Driver's License (International)", "Driver's License (International)"),
        ("Residence Permit", "Residence Permit"),
        ("Social Security Card", "Social Security Card"),
    ]


class Createidprooform(forms.ModelForm):
    Id_proof=forms.MultipleChoiceField(choices=IDI,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Identity
        exclude=("id_proof",)
    def __init__(self,*args,**kwargs):
        user= kwargs.pop("user",None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['residency'].queryset = Residency.objects.filter(created_by=user)
        else:
            self.fields['residency'].queryset=Residency.objects.none()

class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        exclude=("guest","room_details","check_in_date","check_out_date","booked_on")


class Bookingdirectform(forms.ModelForm):

    check_in_date = forms.DateField(
        widget=DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select checki-in-date',
            }
        ),
        label="Check-in-date",
        required=True,
    )

    check_out_date = forms.DateField(
        widget=DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select check-out-date',
            }
        ),
        label="Check-out-date",
        required=True,
    )

    class Meta:
        model = Booking
        exclude = ("guest", "room_details", "check_in_date","check_out_date","booked_on")
    def __init__(self,*args,**kwargs):
        resi_name= kwargs.pop("resi_name",None)
        super().__init__(*args,**kwargs)
        if resi_name:
            self.fields['idproof'].queryset = Identity.objects.filter(residency=resi_name)
        else:
            self.fields['idproof'].queryset=Residency.objects.none()