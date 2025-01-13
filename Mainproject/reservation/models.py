from django.db import models
from accounts.models import Guest
from working.models import Residency, Room_details
import uuid

class Identity(models.Model):
    residency = models.OneToOneField(Residency,on_delete=models.CASCADE)
    id_proof = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.residency} validated {self.id_proof}"


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    total_guest=models.SmallIntegerField()
    room_details = models.ForeignKey(Room_details,on_delete=models.DO_NOTHING)
    check_in_date = models.DateField()
    check_out_date =models.DateField()
    booked_on=models.DateField()
    idproof = models.ForeignKey(Identity, on_delete=models.DO_NOTHING)
    # SDD Amount model and all pejke idher transaction aaiga then aage jaiga n yeah save hoga
    class Meta:
        unique_together = ("room_details","check_in_date")
    
    def __str__(self):
        return f"{self.name} - {self.room_details} ({self.date})"