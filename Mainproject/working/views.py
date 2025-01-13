# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,HttpResponse
from .form import ResidencyForm,Create_Room_forms,CreateRoomTypeForm,SearchForm
from django.views import View
from .models import Residency,Room_details
from django.contrib import messages
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from reservation.models import Booking
from datetime import date

class CreateResidency(LoginRequiredMixin,View):
    login_url='/accounts/login/'
    redirect_field_name='next'
    def get(self,request):

        if request.user.is_staff==True:
            context={
                "title":"Residency",
                "form":ResidencyForm()
            }
            return render(request,"working/form.html",context)

        else:
            return render(request,'unauthorize.html')
    
    def post(self,request):
        form=ResidencyForm(request.POST,request.FILES)
        if form.is_valid():
            residency_insitance=form.save(commit=False)
            residency_insitance.created_by=request.user
            residency_insitance.save()
            return redirect('hoteler')
        return render(request,'working/form.html',{"form":form})


class CreateRoomTyoeview(LoginRequiredMixin,View):
    login_url='/accounts/login/'
    redirect_field_name='next'

    def get(self,request):

        if request.user.is_staff==True:
            context={
            "title":"Create Room Type",
            "form":CreateRoomTypeForm(user=request.user),
            }
            return render(request,"working/form.html",context)
        
        else:
            return render(request,'unauthorize.html')
    
    def post(self,request):
        form=CreateRoomTypeForm(request.POST,request.FILES,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('hoteler')
        return render(request,'working/form.html',{"form":form})


class Create_room_views(LoginRequiredMixin,View):
    login_url='/accounts/login/'
    redirect_field_name='next'

    def get(self,request):
      if request.user.is_staff==True:
            context={
                "title":"Create Room",
                "form":Create_Room_forms(user=request.user)
            }
            return render(request,'working/form.html',context)
      else:
            return render(request,'unauthorize.html')
      
    
    def post(self,request):
        title="Create Rooms Views"
        form=Create_Room_forms(request.POST,request.FILES,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('hoteler')
        print(form.errors)
        return render(request,'working/form.html',{"title":title,"form":form})


def residency_list_view(request):
    if request.user.is_staff==False:
        return render(request,'unauthorize.html')
    resi=Residency.objects.filter(created_by=request.user.id)
    context={
        "resi":resi
    }
    # resi=Residency.objects.all()
    return render(request,"working/yourresidency.html",context)

class allresidencysview(View):
    def get(self,request):
        resi=Residency.objects.all()
        form=SearchForm()
        return render(request,"working/residency_all.html",{"resi":resi,"form":form})
    def post(self,request):
        form=SearchForm(request.POST)
        if form.is_valid():
            namee=form.cleaned_data["search"]
            resi=Residency.objects.filter(
                Q(name__istartswith=namee)|Q(state__istartswith=namee)|Q(city__istartswith=namee)
                  )
            return render(request,"working/residency_all.html",{"resi":resi,"form":form})

            

def rooms_by_residency_foruser(request,residency_id):
    rooms=Room_details.objects.filter(residency__id=residency_id)
    return render(request,'working/all_roomsforuser.html',{'rooms':rooms,"res":residency_id})


def rooms_by_residency(request,residency_id):
    rooms=Room_details.objects.filter(residency_id=residency_id)
    return render(request,'working/all_rooms.html',{'rooms':rooms,'res':residency_id})


def deleteRoom(request,residency_id,room_no):
    deleted=Room_details.objects.filter(residency_id=residency_id , room_no=room_no).delete()
    if deleted:
        messages.success(request,"Succesfully deleted {deleted} Rooms")
        return redirect("all_residency")
    else:
        return HttpResponse("Not able to delete rooms")
    

def deleteResidency(request,residency_id):
    deleted=Residency.objects.filter(id=residency_id).delete()
    messages.success(request,f"Succesfully deleted {deleted} Residency")
    return redirect('all_residency')


class Residency_byState(View):
    def get(self,request,state_name):
        form=SearchForm()
        resi=Residency.objects.filter(state=state_name)  # vasi Bhaiii SUnn bhaii remove St id add state name okay from base.html and url then  hereee ok 
        return render(request,'working/residency_all.html',{'resi':resi,"form":form})
    def post(self,request,state_name):
        form=SearchForm(request.POST)
        if form.is_valid():
            sea=form.cleaned_data['search']
            resi=Residency.objects.filter(
                Q(state=state_name,name__istartswith=sea) | Q(state=state_name,city__istartswith=sea)
    )
            return render(request,'working/residency_all.html',{'resi':resi,"form":form})

def BookingOfYourResidency(request):
    book=Booking.objects.filter(room_details__residency__created_by=request.user)
    return render(request,'reservation/HotelYourBooking.html',{"book":book})


def upcoming_booking(request):
    dated=date.today()
    if request.user.is_staff!=True:
        book=Booking.objects.filter(guest=request.user,check_in_date__gte=dated)
        return render(request,'reservation/yourbooking.html',{"book":book})
    else:
        book=Booking.objects.filter(room_details__residency__created_by=request.user,check_in_date__gte=dated)
        return render(request,'reservation/HotelYourBooking.html',{"book":book})


def privous_booking(request):
    dated=date.today()
    if request.user.is_staff !=True:
        book=Booking.objects.filter(guest=request.user,check_in_date__lt=dated)
        return render(request,'reservation/yourbooking.html',{"book":book})
    else:
        book=Booking.objects.filter(room_details__residency__created_by=request.user,check_in_date__lt=dated)  # .order_by(-"check_in_date")
        return render(request,'reservation/HotelYourBooking.html',{"book":book})