from .models import Booking
from django import forms
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


class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        exclude=("guest","room_details","check_in_date","check_out_date","booked_on","booking_id","payment_status","total_amount")


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
        exclude = ("guest", "room_details", "check_in_date","check_out_date","booked_on","booking_id","payment_status","total_amount")
        