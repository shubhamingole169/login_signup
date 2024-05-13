from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please try another one.")
            return redirect(reverse('home'))
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect(reverse('home'))
            
        if len(username) > 10:
            messages.error(request, "Username must be 10 characters or less.")
            return redirect(reverse('home'))
            
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match.")
            return redirect(reverse('home'))
            
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            return redirect(reverse('home'))
            
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        # Send welcome email
        subject = "Welcome to Our Website"
        message = f"Hello {myuser.first_name}!\n\nWelcome to our website. Thank you for joining us."
        from_email = settings.EMAIL_HOST_USER
        to_email = [myuser.email]
        send_mail(subject, message, from_email, to_email)
        
        messages.success(request, "Your account has been created successfully. Please check your email for confirmation.")
        return redirect(reverse('signin'))
        
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect(reverse('home'))
    
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect(reverse('home'))
