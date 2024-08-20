from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
import smtplib
from django.contrib import messages, auth

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method == 'POST':
        form  = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,
                                               email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()

            #Activating user 
            try:
                current_site =  get_current_site(request)
                mail_subject = "Please activate your account"
                message = render_to_string('accounts/verification_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
            except smtplib.SMTPException as e:
                    # Handle the exception, e.g., log the error, retry, or notify user
                print(f"Error sending email: {e}")
            messages.success(request, 'Registration successful.')
            
            return redirect('account:register')
    else:
        form = RegistrationForm()
   
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('account:login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('account:login')

def activate(request, uidb64,token):
    return 