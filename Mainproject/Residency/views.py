from django.shortcuts import render,redirect
from working.models import Room_details,Residency
from working.models import State
from django.views import View
from reservation.models import Booking
from datetime import date,timedelta
from datetime import datetime



def Hotel_view(request):
    user=request.user
    if user.is_authenticated:
        if user.is_staff==True:
            return render(request,'hotel.html')
        elif user.is_staff!=True:
            return render(request,'unauthorize.html')
    else:
        return redirect('login')
    

# [room_type[0] for room_type in TYPE_NAME_CHOICE]

class Base_view(View):
    def get(self,request):
        state=State.objects.all()
        stat=Residency.objects.values_list('state',flat=True).distinct()
        room_t=Room_details.objects.values_list('room_type__type_name',flat=True).distinct()
        today=date.today()
        formatted_date = today.strftime("%Y-%m-%d")
        max_date= today+timedelta(days=60)
        max_date= max_date.strftime("%Y-%m-%d")
        context={
            'state':state,
            'stat':stat,
            'room_t':room_t,
            "default_date":formatted_date,
            "max_date":max_date
        }
        return render(request,'base.html',context)
    
    def post(self, request):
        state = request.POST.get('state')
        room_type = request.POST.get('room_type')
        checkindate = request.POST.get("Check-in-date")
        checkoutdate = request.POST.get("Check-out-date")
        checkindate = datetime.strptime(checkindate, "%Y-%m-%d").date()
        checkoutdate = datetime.strptime(checkoutdate, "%Y-%m-%d").date()
        if checkoutdate <= checkindate:
            state=State.objects.all()
            stat=Residency.objects.values_list('state',flat=True).distinct()
            room_t=Room_details.objects.values_list('room_type__type_name',flat=True).distinct()
            today=date.today()
            formatted_date = today.strftime("%Y-%m-%d")
            max_date= today+timedelta(days=60)
            max_date= max_date.strftime("%Y-%m-%d")
            mess="Invalid Date Checkout Date Must be AHred of CHeck in date"
            context={
            'state':state,
            'stat':stat,
            'room_t':room_t,
            "default_date":formatted_date,
            "max_date":max_date,
            'mess':mess
        }
            return render(request,'base.html',context)
        rooms = Room_details.objects.filter(residency__state=state, room_type__type_name=room_type)
        booked_room_ids = []
        for ro in rooms:
            existing_bookings = Booking.objects.filter(room_details=ro).values_list(
                'check_in_date', 'check_out_date'
            )

            if not is_room_available(checkindate, checkoutdate, existing_bookings):
                booked_room_ids.append(ro.id)

        return render(request, 'working/room_for_booking.html', {'rooms': rooms, "roomList": booked_room_ids,"checkindate":checkindate,"checkoutdate":checkoutdate})


def is_room_available(new_start, new_end, existing_bookings):
    for existing_start, existing_end in existing_bookings:
        if not (new_end < existing_start or new_start > existing_end):
            return False  
    return True  