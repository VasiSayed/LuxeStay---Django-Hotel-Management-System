from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
# Create your models here.
gender_choice = [
    ("M","Male"),
    ("F","Female"),
    ("O","Other"),
    ("N","Don't want to mention"),
]

class Guest(AbstractUser):
    contact_details = models.CharField(max_length=13,default="",null=False)
    d_o_b = models.DateField(default="",null=False)
    gender = models.CharField(max_length=2,choices=gender_choice,default="N") 
    def save(self,*args,**kwargs):
        if kwargs.get('commit') == False:
            self.d_o_b = date.today()
            user = super().save(*args,**kwargs)
        else:
            self.d_o_b = date.today()
            user = super().save(*args,**kwargs)
        return user 
    class Meta:
        db_table = "Guest"

    def __str__(self):
        return self.username
    
