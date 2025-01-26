from django.urls import path
from . import views

urlpatterns=[
    path('Book-room/<str:checkindate>/<str:checkoutdate>/<int:roomdetails_id>',views.bookingview.as_view(),name="book"),
    path('Final-Booking-rooms/<int:roomdetails_id>',views.BookroomView.as_view(),name='final_booking_rooms'),
    path('booking-recipt/<int:book_id>',views.bookreciptview,name='fullbookrecipt'),
    path('Download-Recipt/<int:id>/invoice',views.GeneratePDF,name="pdf")   
]