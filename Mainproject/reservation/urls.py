from django.urls import path
from . import views

urlpatterns=[
    path('id-proof/',views.Createidproofview.as_view(),name='id_proof'),
    path('see-id-proof',views.Seeidproofs,name="See_id_proof"),
    path('Book-room/<str:checkindate>/<str:checkoutdate>/<int:roomdetails_id>',views.bookingview.as_view(),name="book"),
    path('Final-Booking-rooms/<int:roomdetails_id>',views.BookroomView.as_view(),name='final_booking_rooms'),
    path('YourBoooking/',views.Showbooking,name='Showbook'),
    path('booking-recipt/<int:book_id>',views.bookreciptview,name='fullbookrecipt'),
]