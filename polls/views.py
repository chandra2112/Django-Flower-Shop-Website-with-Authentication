from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .models import contact



# Create your views here.

def home(request):
    if request.method=='POST':
        
        name =request.POST.get('name')
        email =request.POST.get('email')
        number =request.POST.get('number')
        message =request.POST.get('message')
        Contact = contact(name=name,email=email,number=number,message=message)  
        Contact.save()      
    else:
        messages.info(request,"thanks for contact us")
        

    
    return render(request, 'base.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.info(request,"invalid details")
            return redirect("login")
        
        
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']

        if password == repeatpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already used")
                return redirect('register')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username is alredy used")
                return redirect(register)
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
            
        else:
            messages.info(request,"password not the same")
            return redirect('register')



    
    return render(request,'register.html')


def logout_user(request):
    logout(request)
    
    messages.success(request,'you were logged out')
    return redirect('home')


User = get_user_model()

def send_otp_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.info(request,"Email does not exist ")
            return redirect('send_otp_email')  # Redirect to a page showing invalid email

        # Generate the OTP token
        token = default_token_generator.make_token(user)

        # Send the OTP token via email
        subject = 'Your OTP for Password Reset'
        message = f'Dear customer,\n Your OTP is: {token}'
        from_email = settings.EMAIL_HOST_USER  # Replace with your email address
        send_mail(subject, message, from_email, [email])

        # Store the user ID and token in the session
        request.session['user_id'] = user.id
        request.session['otp_token'] = token

        return redirect('verify_otp')

    return render(request, 'send_otp_email.html')


User = get_user_model()

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('user_id')
        token = request.session.get('otp_token')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('invalid_otp')  # Redirect to a page showing invalid OTP

        if default_token_generator.check_token(user, otp):
            request.session['otp_verified'] = True
            return redirect('set_new_password')
        else:
            messages.info(request,"Otp is not exist")
            # return redirect('invalid_otp')  # Redirect to a page showing invalid OTP

    return render(request, 'verify_otp.html')

def set_new_password(request):
    if not request.session.get('otp_verified'):
        return redirect('verify_otp')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user_id = request.session.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('invalid_otp')  # Redirect to a page showing invalid OTP

        # Set the new password for the user
        user.set_password(new_password)
        user.save()

        # Clear the OTP verification session flag and token
        del request.session['otp_verified']
        del request.session['otp_token']
        
        return redirect('login')  # Redirect to a success page after password reset

    return render(request, 'set_new_password.html')