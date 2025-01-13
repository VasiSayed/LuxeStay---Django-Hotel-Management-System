from django.contrib import admin
from .models import Residency,Room_details,Room_type,State
# Register your models here.
admin.site.register([Residency,Room_details,Room_type,State])