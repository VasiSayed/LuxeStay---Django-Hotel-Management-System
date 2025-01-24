from django.shortcuts import render,redirect
from working.models import Room_details,Residency
from working.models import State
from django.views import View
from reservation.models import Booking
from datetime import date,timedelta
from datetime import datetime
from django.contrib import messages


def Hotel_view(request):
    user=request.user
    if user.is_authenticated:
        if user.is_staff==True:
            t_count=Residency.objects.filter(created_by=request.user).count()
            total=Residency.objects.filter(created_by=request.user)
            moonth=datetime.now().month
            year=datetime.now().year
            boook = Booking.objects.filter(room_details__residency__created_by=user,payment_status="Successfull",check_in_date__month=moonth,check_in_date__year=year)
            book_year = Booking.objects.filter(room_details__residency__created_by=user,payment_status="Successfull",check_in_date__year=year)
            monthly=0
            active=0
            yearly=0
            for i in book_year:
                yearly+=i.total_amount

            for i in total:
                if Room_details.objects.filter(residency=i,disable=False).exists():
                    active+=1
            for i in boook:
                monthly+=i.total_amount

            contex={
                "total":t_count,
                "a_count":active,
                "month":monthly,
                'year':yearly,
            }
            return render(request,'hotel.html',contex)
        elif user.is_staff!=True:
            return render(request,'unauthorize.html')
    else:
        return redirect('login')
    

def about(request):
    return render(request,"about.html")

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
            
            context={
            'state':state,
            'stat':stat,
            'room_t':room_t,
            "default_date":formatted_date,
            "max_date":max_date,
        }
            messages.error(request,"Invalid Check_Out-Date cannot be same or before The Check-In_date")
            return render(request,'base.html',context)
        rooms = Room_details.objects.filter(residency__state=state, room_type__type_name=room_type)
        
        booked_room_ids = []
        for ro in rooms:
            existing_bookings = Booking.objects.filter(room_details=ro,payment_status="Successfull").values_list(
                'check_in_date', 'check_out_date'
            )
            ro.room_feature_list=ro.key_features.split(',') if ro.key_features else []
            
            if not is_room_available(checkindate, checkoutdate, existing_bookings):
                booked_room_ids.append(ro.id)

        un_id=[]
        for ro in rooms:
            if ro.no_new==True:
                un_id.append(ro.id)
        return render(request, 'working/room_for_booking.html', {'rooms': rooms, "roomList": booked_room_ids,"checkindate":checkindate,"checkoutdate":checkoutdate,"un":un_id})


def is_room_available(new_start, new_end, existing_bookings):
    for existing_start, existing_end in existing_bookings:
        if not (new_end < existing_start or new_start > existing_end):
            return False  
    return True  