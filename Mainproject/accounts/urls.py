from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("register/<str:registration_for>",views.RegisterView.as_view(),name='register'),
    path("login/",views.LoginView.as_view(),name='login'),
    path('logout/',views.logoutview,name="logout"),
    path('choice/',views.choiceview.as_view(),name='choice'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]