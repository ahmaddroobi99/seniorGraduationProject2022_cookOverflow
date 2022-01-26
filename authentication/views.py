import email

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from cookOverflow import settings


def home(request):
    # return HttpResponse("hello I am Working ")
    return render(request, "authentication/index.html")

def signup (request) :
    # return render(request,"authentication/signup.html")
    if request.method =="POST" :
        username = request.POST['username']
        Bio = request.POST['Bio']
        password = request.POST['password']
        confirm_password =request.POST['confirm_password']
        phone = request.POST['phone']
        email = request.POST['email']


        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')

        if password != confirm_password:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.phone = phone
        myuser.email = email
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to CookOverFlow Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to CookOverFlow!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nDroobi Ataa"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        #
        # # Email Address Confirmation Email
        # current_site = get_current_site(request)
        # email_subject = "Confirm your Email @ GFG - Django Login!!"
        # message2 = render_to_string('email_confirmation.html', {
        #
        #     'name': myuser.first_name,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        #     'token': generate_token.make_token(myuser)
        # })
        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [myuser.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('signup')

    return render(request, "authentication/signout.html")







def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')

def signin (request) :
    # return render(request,"authentication/signin.html")
    if request.method == 'POST' :
        username = request.POST['username']
        password =request.POST['password']

        user =authenticate(username =username,password =password)
        if user is not None :
            login (request,user)
            phone= user.phone
            return render(request, "authentication/index.html" ,{'phone':phone})

        else :
            messages.error(request,"Bad credintioals")
            return redirect("home")

    return render(request,"authenticateion/signout.html")



def signout (request) :
    # return render(request,"authentication/signout.html")

    logout (request)
    messages.success(request,"Logged out sucseffully")
    return redirect('home')

