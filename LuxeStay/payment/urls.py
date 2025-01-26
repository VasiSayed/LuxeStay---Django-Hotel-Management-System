from django.urls import path
from . import views

urlpatterns = [
    path("initiate/<int:booking_id>/", views.initiate_payment, name="initiate_payment"),
    path("callback/<str:razorpay_order_id>/", views.payment_callback, name="payment_callback"),
]
