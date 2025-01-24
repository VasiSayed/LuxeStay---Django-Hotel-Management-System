# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404
from .form import ResidencyForm,Create_Room_forms,CreateRoomTypeForm,SearchForm
from django.views import View
from .models import Residency,Room_details
from django.contrib import messages
from django.db.models import Q
from reservation.models import Booking
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Max


class CreateResidency(LoginRequiredMixin,View):
    login_url='login'

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
            messages.success(request,"succesfully created Residency")
            return redirect('hoteler')
        messages.error(request,"Fill the form correctly")
        for field, errors in form.errors.items():
            messages.error(request, f"{field}: {', '.join(errors)}") 
        return render(request,'working/form.html',{"form":form})


class CreateRoomTyoeview(LoginRequiredMixin,View):
    login_url='login'

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
            messages.success(request,"Sucessfully Created Room Type")
            return redirect('hoteler')
        messages.error(request,"Fill the form correctly")
        for field, errors in form.errors.items():
            messages.error(request, f"{field}: {', '.join(errors)}") 
        return render(request,'working/form.html',{"form":form})


class Create_room_views(LoginRequiredMixin,View):
    login_url='login'

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
            room=form.save(commit=False)
            key=form.cleaned_data["key_features"]
            room.key_features=",".join(key)
            if room.room_type.residency!=room.residency:
                messages.error(request,"Invalid Room type and Residency Match")
                return render(request,'working/form.html',{"title":title,"form":form})
            room.save()
            messages.success(request,"Sucessfully Created Room")
            return redirect('hoteler')
        messages.error(request,"Fill the form correctly")
        for field, errors in form.errors.items():
            messages.error(request, f"{field}: {', '.join(errors)}") 
        return render(request,'working/form.html',{"title":title,"form":form})


@login_required
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
        a=[]
        for i in resi:
            if Room_details.objects.filter(residency__id=i.id).exists()==False:
                a.append(i.id)
            elif Room_details.objects.filter(residency__id=i.id,no_new=False).exists()==False:
                a.append(i.id)
        form=SearchForm()
        return render(request,"working/residency_all.html",{"resi":resi,"form":form,"a":a})
    
    def post(self,request):
        form=SearchForm(request.POST)
        if form.is_valid():
            namee=form.cleaned_data["search"]
            resi=Residency.objects.filter(Q(name__istartswith=namee)|Q(city__istartswith=namee)|Q(state__istartswith=namee))
            a=[]
            for i in resi:
                if Room_details.objects.filter(residency__id=i.id).exists()==False:
                    a.append(i.id)
                elif Room_details.objects.filter(residency__id=i.id,no_new=False).exists()==False:
                    a.append(i.id)                   
            return render(request,"working/residency_all.html",{"resi":resi,"form":form,"a":a})

            

def rooms_by_residency_foruser(request,residency_id):
    dis=[]
    rooms=Room_details.objects.filter(residency__id=residency_id)
    for room in rooms:
        cleaned_features = room.key_features.strip("[]").strip()
        room.key_features_list = [feature.strip() for feature in cleaned_features.split(",")]
    
        if room.no_new==True:
            dis.append(room.id)
    return render(request,'working/all_roomsforuser.html',{'rooms':rooms,"res":residency_id,"dis":dis})



def Avalaiblerooms_residency(request,residency_id):
    rooms=Room_details.objects.filter(residency__id=residency_id,disable=False)
    Cuurent="Avalaible"
    dis=[]
    for room in rooms:
        cleaned_features = room.key_features.strip("[]").strip()
        room.key_features_list = [feature.strip() for feature in cleaned_features.split(",")]
        if room.no_new==True:
            dis.append(room.id)
    return render(request,'working/all_rooms.html',{'rooms':rooms,'res':residency_id,"avalaible_rooms":"ava","dis":dis,"Cuurent":Cuurent})


def deletedrooms_by_resdency(request,residency_id):
    rooms=Room_details.objects.filter(residency__id=residency_id,disable=True)
    Cuurent="Deleted"
    for room in rooms:
        cleaned_features = room.key_features.strip("[]").strip()
        room.key_features_list = [feature.strip() for feature in cleaned_features.split(",")]
    return render(request,'working/all_rooms.html',{'rooms':rooms,'res':residency_id,"not_avalaible_rooms":"not","Cuurent":Cuurent})

from django.conf import settings
def disableeRoom(request,residency_id,room_no):
    if request.user.is_staff==False:
        return render(request,'unauthorize.html')
    room = get_object_or_404(Room_details, id=room_no)
    today=date.today()
    future=Booking.objects.filter(room_details=room, check_in_date__gte=today).aggregate(Max('check_in_date'))
    maxx=future.get('check_in_date__max',None)

    if maxx:
        room.no_new=True
        room.save()
        messages.error(request,f"Your Hotel Has Been Shut for New Bookings ,You Cannot Close Room Because Your Have Future Booking Till {maxx} pls Contact {settings.EMAIL_HOST_USER} for assistance")
        return redirect('rooms_of_residency',f'{residency_id}')
    
    if room.disable == False:
        room.disable=True
        room.no_new=True
        room.save()
        messages.success(request,f"Succesfully disabled Rooms")
        return redirect('rooms_of_residency',f'{residency_id}')

    else:
        messages.error(request,"Room is Already Disabled")
        return redirect('rooms_of_residency',f'{residency_id}')


def AvalaibleRooms(request,residency_id,room_no):
     if request.user.is_staff==False:
        return render(request,'unauthorize.html')
     room= get_object_or_404(Room_details, id=room_no)
     room.no_new=False
     room.disable=False
     room.save()
     messages.success(request,"Room is Sucessfully Avalaible Now For New Booking")
     return redirect('rooms_of_residency',f'{residency_id}')




class Residency_byState(View):
    def get(self,request,state_name):
        form=SearchForm()
        resi=Residency.objects.filter(state=state_name) 
        a=[]
        for i in resi:
            if Room_details.objects.filter(residency__id=i.id).exists() ==False:
                a.append(i.id)
            if Room_details.objects.filter(residency__id=i.id,no_new=False).exists()==False:
                a.append(i.id)
        return render(request,'working/residency_all.html',{'resi':resi,"form":form,"a":a})
    
    def post(self,request,state_name):
        form=SearchForm(request.POST)
        if form.is_valid():
            sea=form.cleaned_data['search']
            resi=Residency.objects.filter(
                Q(state=state_name,name__istartswith=sea) | Q(state=state_name,city__istartswith=sea))
            a=[]
            for i in resi:
                if Room_details.objects.filter(residency__id=i.id).exists()==False:
                    a.append(i.id)
                if Room_details.objects.filter(residency__id=i.id,no_new=False).exists()==False:
                    a.append(i.id)
            return render(request,'working/residency_all.html',{'resi':resi,"form":form,"a":a})
        


@login_required
def upcoming_booking(request):
    dated=date.today()
    if request.user.is_staff!=True:
        book=Booking.objects.filter(guest=request.user,check_in_date__gte=dated,payment_status="Successfull").order_by('check_in_date')
        return render(request,'reservation/yourbooking.html',{"book":book})
    else:
        book=Booking.objects.filter(room_details__residency__created_by=request.user,check_in_date__gte=dated,payment_status="Successfull").order_by('check_in_date')

        return render(request,'reservation/HotelYourBooking.html',{"book":book})


@login_required
def privous_booking(request):
    dated=date.today()
    if request.user.is_staff !=True:
        book=Booking.objects.filter(guest=request.user,check_in_date__lt=dated,payment_status="Successfull").order_by('-check_in_date')
        return render(request,'reservation/yourbooking.html',{"book":book})
    else:
        book=Booking.objects.filter(room_details__residency__created_by=request.user,check_in_date__lt=dated,payment_status="Successfull").order_by('-check_in_date')  # .order_by(-"check_in_date")
        return render(request,'reservation/HotelYourBooking.html',{"book":book})
    
@login_required
def Failed_booking(request):
    if request.user.is_staff==True:
        messages.error(request,"Dear Hotiler This is Your Hotiler Account Please Make Guest Account")
        return redirect('hoteler')
    else:
        book=Booking.objects.filter(guest=request.user,payment_status="Fail").order_by('check_in_date')
        return render(request,'reservation/yourbooking.html',{"book":book,})