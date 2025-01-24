from django.urls import path,include
from . import views

urlpatterns=[
    path('residency/',views.CreateResidency.as_view(),name="residency"),
    path('all-residency-Byresidency/',views.residency_list_view,name="all_residency"),
    path('create-rooms/',views.Create_room_views.as_view(),name="create_rooms"),
    path('rooms/<int:residency_id>',views.Avalaiblerooms_residency,name="rooms_of_residency"),
    path('rooms-user/<int:residency_id>',views.rooms_by_residency_foruser,name="rooms_of_residency_for_user"),
    path('Create-Room-type/',views.CreateRoomTyoeview.as_view(),name="Create_room_type"),
    path('all-residency/',views.allresidencysview.as_view(),name='allResidency'),
    path('Delete-rooms/<int:residency_id>/<int:room_no>',views.disableeRoom,name='delete_room'),
    path('residency-Via-State/<str:state_name>/',views.Residency_byState.as_view(),name='residencyByState'),
    path('reservation/',include('reservation.urls')),
    path('Upcoming-booking',views.upcoming_booking,name="upcoming"),
    path('Previous-booking',views.privous_booking,name="previous"),
    path('Failed-booking',views.Failed_booking,name="fail"),
    path("avalaible-rooms/<int:residency_id>",views.Avalaiblerooms_residency,name="avalaible_rooms"),
    path("disabled-rooms/<int:residency_id>",views.deletedrooms_by_resdency,name="disable"),
    path('avalaible-rooms/<int:residency_id>/<int:room_no>',views.AvalaibleRooms,name="Avalaible Rooms"),
]