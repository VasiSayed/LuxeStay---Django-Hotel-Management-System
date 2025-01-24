from django.db import models
from accounts.models import Guest
from working.models import Residency, Room_details
import uuid
from django.db.models import Q

pay=[
    ("Successfull","Successfull"),
    ("Fail","Fail"),
    ("Pending","Pending")
]

class Booking(models.Model):
    booking_id=models.UUIDField(default=uuid.uuid4,unique=True)
    guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    total_guest=models.SmallIntegerField()
    room_details = models.ForeignKey(Room_details,on_delete=models.DO_NOTHING)
    check_in_date = models.DateField()
    check_out_date =models.DateField()
    total_amount=models.PositiveIntegerField(default=4000,null=False)
    booked_on=models.DateField(auto_now_add=True)
    payment_status=models.CharField(max_length=20,choices=pay,default="Pending")
    # SDD Amount model and all pejke idher transaction aaiga then aage jaiga n yeah save hoga
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["room_details", "check_in_date"],
                    condition=Q(payment_status="Successfull"),
                    name="unique_booking_confirmed"
                )
            ]
    
    def __str__(self):
        return f"{self.name} - {self.room_details}"


    