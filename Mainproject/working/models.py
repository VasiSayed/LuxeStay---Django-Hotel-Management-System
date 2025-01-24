from django.db import models
from accounts.models import Guest
# Create your models here.

STATE_CHOICES = [
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli and Daman and Diu", "Dadra and Nagar Haveli and Daman and Diu"),
    ("Delhi", "Delhi"),
    ("Jammu and Kashmir", "Jammu and Kashmir"),
    ("Ladakh", "Ladakh"),
    ("Lakshadweep", "Lakshadweep"),
    ("Puducherry", "Puducherry")
]



class Residency(models.Model):
    name=models.CharField(max_length=30,null=False,blank=False)
    logo=models.ImageField(upload_to="images/residency/logo")
    area = models.CharField(max_length=50,default="",null=False)
    city = models.CharField(max_length=50,default="",null=False)
    state = models.CharField(max_length=50,choices=STATE_CHOICES,default="Maharashtra",null=False)
    country = models.CharField(max_length=50,default="",null=False)
    created_by=models.ForeignKey(Guest,on_delete=models.CASCADE)
    manage_name=models.CharField(max_length=40,null=False,blank=False)
    contact_no=models.CharField(max_length=10,null=False,blank=False)
    class Meta:
        unique_together=("name","area")
    def __str__(self):
        return f"{self.name}"
    




TYPE_NAME_CHOICE=[
    ("Economy","Economy"),
    ("Standard", "Standard"),
    ("Deluxe", "Deluxe"),
    ("Super Deluxe", "Super Deluxe"),
    ("Suite", "Suite"),
    ("Junior Suite", "Junior Suite"),
    ("Presidential Suite", "Presidential Suite"),
    ("Family Room", "Family Room"),
    ("Studio", "Studio"),
    ("Penthouse", "Penthouse"),
    ]

BED_TYPE_CHOICE=[
    ("King", "King"),
    ("Queen", "Queen"),
    ("Twin", "Twin"),
    ("Single", "Single")
    ]



class Room_type(models.Model):
    residency=models.ForeignKey(Residency,on_delete=models.CASCADE,null=False,blank=False)
    type_name=models.CharField(max_length=30,choices=TYPE_NAME_CHOICE, default="Queen")
    class Meta:
        unique_together=("residency","type_name")
    def __str__(self):
        return f"{self.type_name} In {self.residency.name}"
    
    def Namee(self):
        return f"{self.type_name}"



class Room_details(models.Model):
    residency=models.ForeignKey(Residency,on_delete=models.CASCADE,null=False,blank=False)
    room_type=models.ForeignKey(Room_type,on_delete=models.CASCADE,null=False,blank=False)
    room_no=models.CharField(max_length=10,null=False,blank=False)
    picture=models.ImageField(upload_to="images/residency/roomimages")
    key_features=models.CharField(max_length=200)
    max_guest=models.SmallIntegerField(default=3)
    price_per_night=models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    no_new=models.BooleanField(default=False)
    disable=models.BooleanField(default=False)
    class Meta:
        unique_together=("residency","room_no")
    def __str__(self):
        return f''' Residency :- {self.residency.name}  || Room_type :- {self.room_type.type_name} || Room No :- {self.room_no}'''
    
    
class State(models.Model):
    state=models.CharField(max_length=50,choices=STATE_CHOICES,null=False,unique=True)
    Image=models.ImageField(upload_to='media/images/')
    def __str__(self):
        return f'''{self.state}'''