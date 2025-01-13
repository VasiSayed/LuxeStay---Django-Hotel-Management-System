from django.urls import path,include
from . import views

urlpatterns=[
    path('residency/',views.CreateResidency.as_view(),name="residency"),
    path('all-residency-Byresidency/',views.residency_list_view,name="all_residency"),
    path('create-rooms/',views.Create_room_views.as_view(),name="create_rooms"),
    path('rooms/<int:residency_id>',views.rooms_by_residency,name="rooms_of_residency"),
    path('rooms-user/<int:residency_id>',views.rooms_by_residency_foruser,name="rooms_of_residency_for_user"),
    path('Create-Room-type/',views.CreateRoomTyoeview.as_view(),name="Create_room_type"),
    path('all-residency/',views.allresidencysview.as_view(),name='allResidency'),
    path('Delete-rooms/<int:residency_id>/<int:room_no>',views.deleteRoom,name='delete_room'),
    path('Delete-residency/<int:residency_id>/',views.deleteResidency,name='delete_residency'),
    path('residency-Via-State/<str:state_name>/',views.Residency_byState.as_view(),name='residencyByState'),
    path('reservation/',include('reservation.urls')),
    path('Upcoming-booking',views.upcoming_booking,name="upcoming"),
    path('Previous-booking',views.privous_booking,name="previous"),
    path('Booking-of-your-residency',views.BookingOfYourResidency ,name="bookingofyourresidency"),
]