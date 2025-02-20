"""
URL configuration for Residency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from . import views
from .views import Hotel_view
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('luxeadmin/', admin.site.urls,name="admin"),
    # path('',views.Guest_view,name='index'),
    path("",views.Base_view.as_view(),name='index'),
    # path("", TemplateView.as_view(template_name='base.html'),name="index"),
    path("hotel/", views.Hotel_view,name="hoteler"),
    path('accounts/',include('accounts.urls')),
    path('working/',include('working.urls')),
    path('reservation/',include('reservation.urls')),
    path('about/',views.about,name="about"),
    path("payment/",include('payment.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)