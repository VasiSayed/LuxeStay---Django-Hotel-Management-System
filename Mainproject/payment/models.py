from django.db import models
from accounts.models import Guest
from reservation.models import Booking
# Create your models here.

PAYMENT_STATUS_CHOICE = (
    ('pending','pending'),
    ('Successfull','Successfull'),
    ('Fail','Fail')
)
import uuid
class Payment(models.Model):
    id = models.BigAutoField(primary_key=True,auto_created=True)
    # razorpay_order_id = models.CharField(max_length=25,blank=True,default="default")
    guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING)
    booking = models.ForeignKey(Booking, on_delete=models.DO_NOTHING)
    payment_signature = models.CharField(max_length=64, default='', blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(choices=PAYMENT_STATUS_CHOICE, max_length=20, default='pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.guest} paid {self.amount} - Status: {self.status}"
