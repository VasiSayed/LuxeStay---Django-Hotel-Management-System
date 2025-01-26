from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .form import BookingForm,Bookingdirectform
from .models import Booking
from working.models import Room_details
from datetime import date,timedelta,datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
import pdfkit 

def GeneratePDF(request, id):
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)    
    book = get_object_or_404(Booking, id=id)

    try:
        full_image_url = book.room_details.picture.url
        absolute_image_url = request.build_absolute_uri(full_image_url)
        print(f"Absolute Image URL: {absolute_image_url}")
        html_string = render_to_string('reservation/Print.html', {
            "book": book, 
            "absolute_image_url": absolute_image_url
        })
        options = {
            'enable-local-file-access': True,
            # 'page-size': 'A4',  
            'page-width': '230mm',
            'page-height': '340mm',
        }
        pdf = pdfkit.from_string(html_string, False, options=options, configuration=pdfkit_config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Booking_Invoice_{book.booking_id}.pdf"'
        return response
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return HttpResponse("Failed to generate PDF.", status=500)


class bookingview(LoginRequiredMixin,View):
    login_url='login'

    def get(self,request,checkindate,checkoutdate,roomdetails_id):
        if request.user.is_staff ==True:
            messages.error(request,"Dear Hotiler You Cannot Make a Booking From This Account Please Make Guest Account")
            return redirect('hoteler')
        room=Room_details.objects.get(id=roomdetails_id)
        try:
                checkindate = datetime.strptime(checkindate, "%b. %d, %Y").date()
                checkoutdate = datetime.strptime(checkoutdate, "%b. %d, %Y").date()
        except Exception:
                checkindate = datetime.strptime(checkindate, "%B %d, %Y").date()
                checkoutdate = datetime.strptime(checkoutdate, "%B %d, %Y").date()
        duration=(checkoutdate-checkindate).days
        total_amou=duration*room.price_per_night
        title="Book Room"
        form=BookingForm()
        return render(request,'reservation/form.html',{"form":form,"title":title,"total":total_amou})
    
    def post(self,request,checkindate,checkoutdate,roomdetails_id):
        form=BookingForm(request.POST)
        title="Book Room"
        if form.is_valid():
            ro=Room_details.objects.get(id=roomdetails_id)
            rot=ro.max_guest
            book=form.save(commit=False)
            if book.total_guest <=0:
                messages.error(request,"No of Guest Cannot Be zero or Less THen Zero")
                return render(request,'reservation/form.html',{"form":form,"title":title})

            if book.total_guest >rot :
                messages.error(request,f"Invalid ! Maximum Guest : {rot}")
                return render(request,'reservation/form.html',{"form":form,"title":title})
            room=Room_details.objects.get(id=roomdetails_id)
            try:
                checkindate = datetime.strptime(checkindate, "%b. %d, %Y").date()
                checkoutdate = datetime.strptime(checkoutdate, "%b. %d, %Y").date()
            except Exception:
                checkindate = datetime.strptime(checkindate, "%B %d, %Y").date()
                checkoutdate = datetime.strptime(checkoutdate, "%B %d, %Y").date()
            duration=(checkoutdate-checkindate).days
            total_amou=duration*room.price_per_night
            book.check_in_date = checkindate
            book.check_out_date = checkoutdate
            book.guest=request.user
            book.room_details=room
            book.booked_on=date.today()
            book.total_amount=total_amou
            book.save()
            idd=book.id
            book=Booking.objects.get(id=idd)
            messages.success(request,"Booking Succesfull")
            return redirect('initiate_payment', booking_id=idd) 
             
        messages.error(request,"Fill the form correctly")
        return render(request, 'reservation/form.html', {"form": form,"title":title})
    

# class BookroomView(LoginRequiredMixin,View):
#     login_url='login'
#     def get(self, request, roomdetails_id):
#         rooms = Room_details.objects.get(id=roomdetails_id)
#         now_date = date.today()
#         formatted_date = now_date.strftime("%Y-%m-%d")
#         max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
#         form = Bookingdirectform()
#         return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"formatted_date": formatted_date,"max_date": max_date})

#     def post(self, request, roomdetails_id):
#         form = Bookingdirectform(request.POST)
#         if form.is_valid():
#             checkindate = form.cleaned_data.get("check_in_date")
#             checkoutdate = form.cleaned_data.get("check_out_date")
#             if checkoutdate<checkindate:
#                 rooms = Room_details.objects.get(id=roomdetails_id)
#                 now_date = date.today()
#                 formatted_date = now_date.strftime("%Y-%m-%d")
#                 max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
#                 context={
#                     "rooms": rooms,
#                     "form": form,
#                     "formatted_date": formatted_date,
#                     "max_date": max_date,
#                 }
#                 messages.error(request,"Check-Out-Date cannot be before Check-In-Date")
#                 return render(request,"reservation/Indirectroombooking.html",context)
            
#             fo = form.save(commit=False)
#             rooms = Room_details.objects.get(id=roomdetails_id)

#             total_guest = int(fo.total_guest)
#             if total_guest <= 0:
#                 now_date = date.today()
#                 formatted_date = now_date.strftime("%Y-%m-%d")
#                 max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
#                 messages.error(request,"No of Guest Cannot Be zero or Less THen Zero")
#                 return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"formatted_date": formatted_date,"max_date": max_date,})
            
#             rot=rooms.max_guest
#             if total_guest>rot:
#                 now_date = date.today()
#                 formatted_date = now_date.strftime("%Y-%m-%d")
#                 max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
#                 messages.error(request,f"Invalid ! Maximum Guest : {rot}")
#                 return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"formatted_date": formatted_date,"max_date": max_date,})  
                          
#             existing_bookings = Booking.objects.filter(room_details__id=roomdetails_id).values_list('check_in_date', 'check_out_date')
#             if not is_room_available(checkindate, checkoutdate, existing_bookings):
#                 now_date = date.today()
#                 formatted_date = now_date.strftime("%Y-%m-%d")
#                 max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
#                 messages.error(request,"Not Available On The Entered Date")
#                 return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"formatted_date": formatted_date,"max_date": max_date,})
            
#             room=Room_details.objects.get(id=roomdetails_id)
#             fo.room_details =room
#             duration=(checkoutdate-checkindate).days
#             total_amou=duration*room.price_per_night
#             resi = fo.room_details.residency.name
#             type = fo.room_details.room_type.type_name
#             phone = fo.room_details.residency.contact_no
#             fo.guest = request.user
#             email = request.user.email
#             fo.check_in_date=checkindate
#             fo.check_out_date=checkoutdate
#             bookon=date.today()
#             fo.booked_on=bookon
#             fo.total_amount=total_amou
#             fo.save()
#             bo_id=fo.id
#             send_mail(
#                 f''' Booking Confirmation - {resi}''',
#                 f'''Thank you for booking with {resi}! We’re excited to confirm your reservation.

# Booking Details:

# Date: {checkindate}
# Room Type: {type}

# Important Information:
# ID Proof Required: Please carry a valid government-issued ID for check-in.

# We hope you have a pleasant and hassle-free stay! Should you need assistance, feel free to contact the hotel at {phone}.

# Looking forward to welcoming you!

# Best regards,
# Residency Team''', settings.DEFAULT_FROM_EMAIL, {email}, True)

#             book = Booking.objects.get(id=bo_id)
#             messages.success(request,"Booking succefull")
#             return render(request, "reservation/comfirmBookedPage.html", {"book":book})
#         else:
#             now_date = date.today()
#             formatted_date = now_date.strftime("%Y-%m-%d")
#             max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
#             messages.error(request,"Fill The Form Correctly")
#             rooms = Room_details.objects.filter(id=roomdetails_id)
#             return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms,"form": form,"Mess": "Invalid Form Data","formatted_date": formatted_date,"max_date": max_date,})
        



class BookroomView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, roomdetails_id):
        if request.user.is_staff ==True:
            messages.error(request,"Dear Hotiler You Cannot Make a Booking From This Account Please Make Guest Account")
            return redirect('hoteler')
        rooms = Room_details.objects.get(id=roomdetails_id)
        now_date = date.today()
        formatted_date = now_date.strftime("%Y-%m-%d")
        max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
        form = Bookingdirectform()
        cleaned_features = rooms.key_features.strip("[]").strip()
        rooms.key_features_list = [feature.strip() for feature in cleaned_features.split(",")]
        return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms, "form": form, "formatted_date": formatted_date, "max_date": max_date})

    def post(self, request, roomdetails_id):
        form = Bookingdirectform(request.POST)
        if form.is_valid():
            checkindate = form.cleaned_data.get("check_in_date")
            checkoutdate = form.cleaned_data.get("check_out_date")
            if checkoutdate <= checkindate:
                rooms = Room_details.objects.get(id=roomdetails_id)
                now_date = date.today()
                formatted_date = now_date.strftime("%Y-%m-%d")
                max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
                context = {
                    "rooms": rooms,
                    "form": form,
                    "formatted_date": formatted_date,
                    "max_date": max_date,
                }
                messages.error(request, "Check-Out-Date cannot be before or same to Check-In-Date")
                return render(request, "reservation/Indirectroombooking.html", context)
            
            fo = form.save(commit=False)
            rooms = Room_details.objects.get(id=roomdetails_id)
            total_guest = int(fo.total_guest)
            if total_guest <= 0:
                now_date = date.today()
                formatted_date = now_date.strftime("%Y-%m-%d")
                max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
                messages.error(request, "No of Guest Cannot Be zero or Less Than Zero")
                return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms, "form": form, "formatted_date": formatted_date, "max_date": max_date})
            
            rot = rooms.max_guest
            if total_guest > rot:
                now_date = date.today()
                formatted_date = now_date.strftime("%Y-%m-%d")
                max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
                messages.error(request, f"Invalid ! Maximum Guest : {rot}")
                return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms, "form": form, "formatted_date": formatted_date, "max_date": max_date})

            existing_bookings = Booking.objects.filter(room_details__id=roomdetails_id,payment_status="Successfull").values_list('check_in_date', 'check_out_date')
            if not is_room_available(checkindate, checkoutdate, existing_bookings):
                now_date = date.today()
                formatted_date = now_date.strftime("%Y-%m-%d")
                max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
                messages.error(request, "Not Available On The Entered Date")
                return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms, "form": form, "formatted_date": formatted_date, "max_date": max_date})
            
            room = Room_details.objects.get(id=roomdetails_id)
            fo.room_details = room
            duration = (checkoutdate - checkindate).days
            total_amou = duration * room.price_per_night
            fo.guest = request.user
            fo.check_in_date = checkindate
            fo.check_out_date = checkoutdate
            fo.booked_on = date.today()
            fo.total_amount = total_amou
            fo.save()

            return redirect('initiate_payment', booking_id=fo.id) 

        else:
            now_date = date.today()
            formatted_date = now_date.strftime("%Y-%m-%d")
            max_date = (now_date + timedelta(days=60)).strftime("%Y-%m-%d")
            rooms = Room_details.objects.filter(id=roomdetails_id)
            messages.error(request, "Fill The Form Correctly")
            return render(request, "reservation/Indirectroombooking.html", {"rooms": rooms, "form": form, "formatted_date": formatted_date, "max_date": max_date})













def is_room_available(new_start, new_end, existing_bookings):
    for existing_start, existing_end in existing_bookings:
        if not (new_end < existing_start or new_start > existing_end):
            return False  
    return True  


def bookreciptview(request,book_id):
    if request.user.is_staff!=True:
        book=Booking.objects.get(id=book_id)
        return render(request,'reservation/comfirmBookedPage.html',{"book":book})
    else:
        book=Booking.objects.get(id=book_id)
        return render(request,'reservation/comfirmhotelPage.html',{"book":book})

