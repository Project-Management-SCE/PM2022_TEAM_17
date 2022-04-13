from email import message
from re import A
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from requests import request
from .forms import CreateNewAgent
from .models import Agent, Customer
from django.contrib import messages
# Create your views here.
from accounts.models import User
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required


def CustomerSignIn(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            cust = User.objects.get(email = emailCheck,password = passwordCheck,is_Customer=True)
        except User.DoesNotExist: # if customer with such email or password doesn't exists or some of the data is wrong
            return render(response, "CustomerSignUp/signin_page.html", {'alert': True})
        if cust is not None:
            auth.login(response, cust)
            messages.success(response,"Sign in successfully!")
            return redirect('/')
            #return render(response, "AgentSignUp/home.html", {})
        else:
            return render(response, "CustomerSignUp/signin_page.html", {'alert': True})
    else:
        return render(response, "CustomerSignUp/signin_page.html", {})

def CustomerSignUp(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        #cust = Customer()
        full_name = response.POST.get('full_name')
        email = response.POST.get('email')
        password = response.POST.get('password')
        pass2 = response.POST.get('password2')
        city = response.POST.get('city')
        Mobile = response.POST.get('Mobile')
        try:
            custEmailTest = User.objects.get(email = email,is_Customer=True)
        except User.DoesNotExist:
            custEmailTest = None
            #return render(response, "CustomerSignUp/signup_page.html", {'alert_email': True})
        if password == pass2:
            if not custEmailTest:
                cust=User.objects.create_Customer(full_name=full_name,email=email,password=password,city=city,Mobile=Mobile)
                cust.save()
                return redirect("/home")
            else:
                return render(response, "CustomerSignUp/signup_page.html", {'alert_email': True})
        elif password != pass2:
            return render(response, "CustomerSignUp/signup_page.html", {'alert_pass': True})
    else:
        return render(response, "CustomerSignUp/signup_page.html", {})


def AgentSignIn(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            agent = User.objects.get(email = emailCheck,password = passwordCheck,is_Agent=True)
        except User.DoesNotExist: # if agent with such email or password doesn't exists or some of the data is wrong
            messages.error(response, "one or more of the credentials are incorrect!")
            return redirect("/agent_signin")
        if agent is not None:
            auth.login(response, agent)
            messages.success(response, "Sign in successfully!")
            return redirect("/agent_signin") 
    else:
        return render(response, "AgentSignUp/signin_page.html", {})
        
def AgentSignUp(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        #agent = User()
        full_name = response.POST.get('full_name')
        email = response.POST.get('email')
        password = response.POST.get('password')
        pass2 = response.POST.get('password2')
        city = response.POST.get('city')
        Mobile = response.POST.get('Mobile')
        #isConfirmedAgent = False
        try:
            agentEmailTest = User.objects.get(email = email,is_Agent=True)
        except User.DoesNotExist:
            agentEmailTest=None 
        if password == pass2:
            if not agentEmailTest:
                agent=User.objects.create_Agent(full_name=full_name,email=email,password=password,city=city,Mobile=Mobile)
                agent.save()
                return redirect("/home")
            else:
                return render(response, "AgentSignUp/signup_page.html", {'alert_email': True})
        elif password != pass2:
            return render(response, "AgentSignUp/signup_page.html", {'alert_pass': True})
            
    else:
        form = CreateNewAgent()
    return render(response, "AgentSignUp/signup_page.html", {"form":form})

def home(response):
    return render(response, "AgentSignUp/home.html", {})

def AdminSignIn(response):
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            admin = User.objects.get(email = emailCheck,password = passwordCheck,is_Admin=True)
        except User.DoesNotExist: # if agent with such email or password doesn't exists or some of the data is wrong
            messages.error(response, "one or more of the credentials are incorrect!")
            return redirect("/admin_signin")
        if admin is not None:
            auth.login(response, admin)
            messages.success(response, "Sign in successfully!")
            return redirect("/admin_homepage") 
    else:
        return render(response, "AdminSignIn/admin_signin.html", {})

def AdminHomePage(request):
    Id = request.user.email
    admin = User.objects.get(email=Id)
    if admin.is_Admin ==True:
        return render(request, "AdminHomePage/admin_homepage.html", {})
    return redirect("/home")