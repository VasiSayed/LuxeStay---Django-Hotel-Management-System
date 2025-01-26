from django.shortcuts import render,redirect
from .form import LoginForm,RegistrationForm,ChangePasswordFOrm
from django.views import View
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from datetime import date
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
# Create your views here.

class ChangePassword(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        form=ChangePasswordFOrm()
        context={
        "title":"Password Change Form",
        "form":form
        }

        return render(request,"accounts/login.html",context)
    def post(self, request):
        form = ChangePasswordFOrm(request.POST)
        context={
                    "title":"Password Change Form",
                    "form":form
                    }
        
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data['Current_Password']
            new_password = form.cleaned_data['New_Password']
            confirm_password = form.cleaned_data['Comfirm_Password']
 
            if not user.check_password(current_password):
                messages.error(request, "Incorrect current password. Please try again.")
                return render(request, "accounts/change_password.html",context)

            if new_password != confirm_password:
                messages.error(request, "New password and confirm password do not match.")
                return render(request, "accounts/change_password.html",context)

            if user.username.lower() in new_password.lower():
                messages.error(request, "New password cannot contain your username.")
                return render(request, "accounts/change_password.html",context)

            if current_password == new_password:
                messages.error(request, "New password cannot be the same as the current password.")
                return render(request, "accounts/change_password.html",context)

            try:
                password_validation.validate_password(new_password, user=user)
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
                context={
                    "title":"CHange Password",
                    "form":form
                    }
                return render(request, "accounts/change_password.html", context)

            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password successfully changed.")
            return redirect('index')

        else:
            context={
                "title":"CHange Password",
                "form":form
                }
            messages.error(request, "Please fill the form correctly.")
            return render(request, "accounts/change_password.html",context)


class RegisterView(View):
    def get(self,request,registration_for="Guest"):
        form=RegistrationForm()
        title="Register Form"
        return render(request,"accounts/register.html",{"form":form,"title":title})
    
    def post(self,request,registration_for="Guest"):
        form=RegistrationForm(request.POST)
        title="Register Form"
        if form.is_valid():
           user=form.save(commit=False)
           da=date.today()
           year_back= da - timedelta(days=18*365)
           if user.d_o_b >da:
               messages.error(request,"DOB Cannot be a Future Date")
               return render(request,'accounts/register.html',{"form":form,"title":title})
           
           if user.d_o_b > year_back:
               messages.error(request,"Minnimum Age should be 18")
               return render(request,'accounts/register.html',{"form":form,"title":title})
           
           user.is_staff = True if registration_for=="Hotel" else False 
           user.save()
           username=user.username
           email=user.email
           if user.is_staff==False:
            messages.success(request,f"Dear Guest : {username} Registraion Successfull")
            send_mail("Welcome to Residency - Registration Successful!"
                        ,f'''Dear {username},

    Thank you for registering with Residency, your trusted platform for short stays and comfortable accommodations, just like a home away from home.

    We are thrilled to have you join our community. Your account is now active, and you can start exploring our wide range of stays tailored to your preferences.

    Account Details
    Username: {username}
    Registered Email: {email}
    What's Next?
    Explore our Top Stays to find your perfect match.
    Book your stay in a few simple clicks.
    Enjoy a seamless and memorable experience with Residency!
    if you have any questions or need assistance, feel free to reach out to us at support@residency.com.

    We hope you have an amazing experience!

    Warm regards,
    The Residency Team''',"flowstudioworks@gmail.com",[email],True)
           else:
                messages.success(request,f"Dear Hotilier : {username} Registraion Successfull")
                send_mail(
                "Welcome to Residency - Start Listing Your Hotel!",
                f'''Dear {username},

            Thank you for joining **Residency** as a host! We’re thrilled to have you onboard and can't wait to help you connect with travelers from around the globe.

### What's Next?
2. **Showcase Your Rooms**: Provide detailed information about the rooms you offer, including pricing, amenities, and photos, to attract more guests.
3. **Go Live**: Once your property is approved, it will be visible to thousands of travelers searching for the perfect stay.

### Why List on Residency?
- Reach a global audience of travelers.
- Manage your bookings with ease through our user-friendly dashboard.
- Build trust with reviews and ratings from happy guests.

Get started today by clicking the link below to list your property:
**[List Your Property](your-listing-url.com)**

If you have any questions or need assistance, our support team is here to help. Feel free to contact us anytime at **support@residency.com**.

Let’s make your hosting journey successful and rewarding!

Warm regards,  
**The Residency Team**

---
This is an automated email. Please do not reply directly to this message.
''' ,"flowstudioworks@gmail.com",[email],True)
           return redirect("login")
        else:
            messages.error(request,"fill the forms correctly")
            return render(request,"accounts/register.html",{"form":form,"title":title})
        

class LoginView(View):
    def get(self,request):
        form=LoginForm()
        title="Login Form"
        return render(request,"accounts/login.html",{"form":form,"title":title})
    
    def post(self,request):
        redirect_field_name=request.GET.get('next') if request.GET.get('next') else ""
        form=LoginForm(request.POST)
        title="Login Form"
        if form.is_valid():
            user=authenticate(request=request,
                              username = form.cleaned_data['username'], 
                              password= form.cleaned_data['password'])
            if user:
                login(request,user)
                username=user.username
                email=user.email
                messages.success(request,"Login In Successfull")
                if redirect_field_name:
                    return redirect(redirect_field_name)
                if user.is_staff==True:

                    send_mail("Login Successful - Welcome Back to Residency",
                              f'''Dear {username},

Your login to **Residency** was successful! We're happy to have you back managing your listings and connecting with travelers.

### Next Steps:
- **Manage Your Hotel**: Update your hotel details, availability, and pricing.
- **View Bookings**: Check and respond to guest bookings in your dashboard.
- **Enhance Your Listing**: Make your property stand out with great photos and competitive rates.


If this login wasn’t made by you, please reset your password immediately or contact our support team at **support@residency.com**.

Warm regards,  
**The Residency Team**  
''',"vasisayed09421@gmail.com",{email},True)
                    return redirect('hoteler')
                else:
                    send_mail("Login Successful - Welcome Back to Residency",
                               f'''Dear {username},

Your login to **Residency** was successful! We're excited to help you find your next perfect stay.

### What You Can Do Now:
- **Explore Hotels**: Browse top-rated properties tailored to your preferences.
- **Manage Bookings**: View, update, or cancel your upcoming reservations.
- **Exclusive Offers**: Check out the latest deals and discounts.

Start exploring here:  
**[Login to Your Account](guest-dashboard-url.com)**

If this login wasn’t made by you, please reset your password immediately or contact our support team at **support@residency.com**.

Warm regards,  
**The Residency Team**  
''',"vasisayed09421@gmail.com",{email},True)
                    return redirect('index')
            messages.error(request,"Invalid Username Or Password")
            return render(request,'accounts/login.html',{"form":form,"title":title})
        else:
            messages.success(request,"Successfully Login")
            return render(request,"accounts/login.html",{"form":form,"title":title})
        
def logoutview(request):
    logout(request)
    messages.success(request,"Succesfully Logout")
    return redirect('index')

class choiceview(View):
    def get(self,request):
        return render(request,'accounts/choice.html')
    
    def post(self,request):
        response=request.POST
        if response.get("choice")=="List Hotel":
            return redirect('register',"Hotel")

        elif response.get("choice")=='Book Hotel':
            return redirect('register','Guest')
        
        else:
            error_message = "Please make a valid selection."
            return render(request, 'accounts/choice.html', {'error': error_message})