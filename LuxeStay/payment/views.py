from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from .models import Payment, Booking
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import razorpay
import pkg_resources

def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount_in_paise = int(booking.total_amount * 100)  
    currency = 'INR'
    payment_capture = 1
    checkin=booking.check_in_date
    checkout=booking.check_out_date
    order_data = {
        "amount": amount_in_paise,
        "currency": currency,
        "payment_capture": payment_capture,
    }
    razorpay_order = client.order.create(data=order_data)

    payment = Payment.objects.create(
        guest=booking.guest,
        booking=booking,
        amount=booking.total_amount,
        status='pending',
        razorpay_order_id=razorpay_order['id']
    )

    context = {
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": razorpay_order['id'],
        "amount":booking.total_amount,  
        "amount_in_paise": amount_in_paise,  
        "currency": currency,
        "callback_url": f"/payment/callback/{razorpay_order['id'],}/",  
        'checkout':checkout,
        'checkin':checkin,
    }
    return render(request, "payment/initiate_payment.html", context)


@csrf_exempt
def payment_callback(request,razorpay_order_id ):
    payment = get_object_or_404(Payment,razorpay_order_id =razorpay_order_id )
    booking = payment.booking  

    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        print("POST Data:", request.POST)

        params = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        try:
            if razorpay_order_id != payment.razorpay_order_id:
                raise Exception("Razorpay Order ID mismatch")

            client.utility.verify_payment_signature(params)

            payment.status = 'Successfull'
            payment.razorpay_payment_id = razorpay_payment_id
            payment.payment_signature = razorpay_signature
            payment.save()
            booking.payment_status = "Successfull"  
            booking.save()
        
            
            
            send_mail(subject = f"Booking Confirmation: Room {booking.room_details.room_no} in {booking.room_details.residency.name}",
    message = f"""
    Dear Hotelier {booking.room_details.residency.name},

    We are pleased to inform you that one of your rooms has been booked:

    - **Hotel Name**: {booking.room_details.residency.name}
    - **Room Number**: {booking.room_details.room_no}
    - **Room Type**: {booking.room_details.room_type}
    - **Guest Name**: {booking.name}
    - **Check-in Date**: {booking.check_in_date}
    - **Check-out Date**: {booking.check_out_date}

    Please prepare the room accordingly and ensure the guest has a pleasant stay.

    Best Regards,
    LuxeStay
    """,from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.room_details.residency.created_by.email],  
                fail_silently=False)
            
            send_mail(
                subject=f'"Booking Confirmation: Room {booking.room_details.room_no},Room Type {booking.room_details.room_type} in {booking.room_details.residency}',
                message=f'''Thank you for booking with us! We’re excited to confirm your reservation.

Booking Details:
- Check-in Date: {booking.check_in_date}
- Check-out Date: {booking.check_out_date}
- Room: {booking.room_details}

Important Information:
Please carry a valid government-issued ID for check-in.

We hope you have a pleasant and hassle-free stay! Should you need assistance, feel free to contact us.

Best regards,
Residency Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.guest.email],  
                fail_silently=False
            )


            return render(request, "reservation/comfirmBookedPage.html", {"book": booking})

        except razorpay.errors.SignatureVerificationError as e:
            print(f"Signature Verification Error: {str(e)}")

            payment.status = 'Fail'
            payment.save()

            booking.payment_status = "Fail"
            booking.save()

            return render(request, "payment/failed.html", {"payment": payment})

        except Exception as e:
            print(f"Error: {str(e)}")
            payment.status = 'Fail'
            payment.save()
            booking.payment_status = "Fail"
            booking.save()
            return render(request, "payment/failed.html", {"payment": payment})

    elif request.method == "GET":
        if payment.status == "Successfull" and booking.payment_status == "Successfull":
            return render(request, "reservation/comfirmBookedPage.html", {"book": booking})
        else:
            return render(request, "payment/failed.html", {"payment": payment})

    return HttpResponse("Invalid request method", status=405)
