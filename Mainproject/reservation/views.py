from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views import View
from .form import Createidprooform,BookingForm,Bookingdirectform
from .models import Identity,Booking
from working.models import Room_details,Residency
from datetime import date,timedelta,datetime
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

class Createidproofview(View):
    def get(self,request):
        context={
            "title":"Id Proof",
            "form":Createidprooform(user=request.user)
        }
        return render(request,"reservation/form.html",context)
    
    def post(self,request):
        title="Id Proof acceptable for your residency"
        form=Createidprooform(request.POST,user=request.user)
        if form.is_valid():
            re=form.cleaned_data.get("residency")
            ids=form.cleaned_data.get("Id_proof")
            use=Identity(residency=re,id_proof=ids)
            use.save()
            return redirect('hoteler')
        print(form.errors)
        return render(request,"reservation/form.html",{"title":title,"form":form})


def Seeidproofs(request):
    idproof=Identity.objects.filter(residency__created_by=request.user)
    return render(request,"reservation/residency_idproof.html",{"idproof":idproof})

   
class bookingview(LoginRequiredMixin,View):
    login_url='login'
    redirect_field_name='next'

    def get(self,request,checkindate,checkoutdate,roomdetails_id):
        form=BookingForm()
        return render(request,'reservation/form.html',{"form":form})
    
    def post(self,request,checkindate,checkoutdate,roomdetails_id):
        form=BookingForm(request.POST)
        if form.is_valid():
            book=form.save(commit=False)
            if book.total_guest<=0 :
                mess="Invalid No of Guest"
                return render(request,'reservation/form.html',{"form":form,"mess":mess})
            room=Room_details.objects.get(id=roomdetails_id)
            checkindate = datetime.strptime(checkindate, "%b. %d, %Y").date()
            checkoutdate = datetime.strptime(checkoutdate, "%b. %d, %Y").date()
            book.check_in_date = checkindate
            book.check_out_date = checkoutdate
            book.guest=request.user
            book.room_details=room
            book.booked_on=date.today()
            book.save()
            name=book.name
            book_on=book.booked_on
            return render(request,'reservation/BookedPage.html',{"room":room,"date":date,"name":name,"bookdate":book_on,"checkindate":checkindate,"checkoutdate":checkoutdate})
        return render(request, 'reservation/form.html', {"form": form})
    

class BookroomView(LoginRequiredMixin,View):
    login_url='login'
    def get(self, request, roomdetails_id):
       
        rooms = Room_details.objects.filter(id=roomdetails_id)
        now_date = date.today()
        formatted_date = now_date.strftime("%Y-%m-%d")
        max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
        resi_name=Room_details.objects.get(id=roomdetails_id).residency
        form = Bookingdirectform(resi_name=resi_name)
        return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"formatted_date": formatted_date,"max_date": max_date})

    def post(self, request, roomdetails_id):
        resi_name=Room_details.objects.get(id=roomdetails_id).residency
        form = Bookingdirectform(request.POST,resi_name=resi_name)
        if form.is_valid():
            checkindate = form.cleaned_data.get("check_in_date")
            checkoutdate = form.cleaned_data.get("check_out_date")
            fo = form.save(commit=False)
            fo.check_in_date=checkindate
            fo.check_out_date=checkoutdate

            total_guest = int(fo.total_guest)
            if total_guest <= 0:
                rooms = Room_details.objects.filter(id=roomdetails_id)
                return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"Mess": "Invalid No of Guests",})

            existing_bookings = Booking.objects.filter(room_details__id=roomdetails_id).values_list('check_in_date', 'check_out_date')
            if not is_room_available(checkindate, checkoutdate, existing_bookings):
                rooms = Room_details.objects.filter(id=roomdetails_id)
                return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"Mess": "Not Available On The Entered Date",})
            room=Room_details.objects.get(id=roomdetails_id)
            fo.room_details =room
            resi = fo.room_details.residency.name
            type = fo.room_details.room_type.type_name
            phone = fo.room_details.residency.contact_no
            fo.guest = request.user
            email = request.user.email
            bookon=date.today()
            fo.booked_on=bookon
            fo.save()

            send_mail(
                f''' Booking Confirmation - {resi}''',
                f'''Thank you for booking with {resi}! We’re excited to confirm your reservation.

Booking Details:

Date: {checkindate}
Room Type: {type}

Important Information:
ID Proof Required: Please carry a valid government-issued ID for check-in.

We hope you have a pleasant and hassle-free stay! Should you need assistance, feel free to contact the hotel at {phone}.

Looking forward to welcoming you!

Best regards,
Residency Team''', settings.DEFAULT_FROM_EMAIL, {email}, True)

            room = Room_details.objects.get(id=roomdetails_id)
            return render(request, "reservation/BookedPage.html", {"room": room,"checkindate": checkindate,"checkoutdate":checkoutdate,"bookdate":bookon,"name": fo.name,})
        else:
            rooms = Room_details.objects.filter(id=roomdetails_id)
            return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"Mess": "Invalid Form Data"})
        
def is_room_available(new_start, new_end, existing_bookings):
    for existing_start, existing_end in existing_bookings:
        if not (new_end < existing_start or new_start > existing_end):
            return False  
    return True  



def Showbooking(request):
    book=Booking.objects.filter(guest=request.user.id).order_by('check_in_date')
    return render(request,"reservation/yourbooking.html",{"book":book})


def bookreciptview(request,book_id):
    book=Booking.objects.get(id=book_id)
    name=book.name
    checkindate=book.check_in_date
    checkoutdate=book.check_out_date
    bookon=book.booked_on
    room=book.room_details
    return render(request,'reservation/Bookedpage.html',{"room":room,"name":name,"checkoutdate":checkoutdate,"checkindate":checkindate,"bookdate":bookon})
