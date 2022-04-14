from email import message
from re import A

from typing import List
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from requests import request
from .forms import CreateNewAgent
from django.contrib import messages
# Create your views here.
from accounts.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


def CustomerSignIn(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            cust = User.objects.get(email = emailCheck,password = passwordCheck,is_Customer=True)
        except User.DoesNotExist: # if customer with such email or password doesn't exists or some of the data is wrong
            messages.error(response, "one or more of the credentials are incorrect!")
            return redirect("/cust_signin")
        if cust is not None:
            login(response, cust)
            messages.success(response,"Sign in successfully!")
            cust.is_active = True
            return redirect('/')
            #return render(response, "AgentSignUp/home.html", {})
        else:
            
            return render(response, "CustomerSignUp/signin_page.html", {})
    else:
        return render(response, "CustomerSignUp/signin_page.html", {})

def CustomerSignUp(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        #cust = Customer()
        username = response.POST.get('username')
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
                cust=User.objects.create_Customer(username=username,full_name=full_name,email=email,password=password,city=city,Mobile=Mobile)
                cust.save()
                return redirect("/home")
            else:
                return render(response, "CustomerSignUp/signup_page.html", {})
        elif password != pass2:
            return render(response, "CustomerSignUp/signup_page.html", {})
    else:
        return render(response, "CustomerSignUp/signup_page.html", {})


def AgentSignIn(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        emailCheck = response.POST.get('email')
        passwordCheck = response.POST.get('password')
        try:
            agent = User.objects.get(email = emailCheck,password = passwordCheck)
        except User.DoesNotExist: # if agent with such email or password doesn't exists or some of the data is wrong
            messages.error(response, "one or more of the credentials are incorrect!")
            return redirect("/agent_signin")
        if agent is not None:
            login(response, agent)
            messages.success(response, "Sign in successfully!")

            agent.is_active = True
            return redirect("/") 

            return redirect("/home") 

    else:
        return render(response, "AgentSignUp/signin_page.html", {})

    # if(request.user.is_authenticated):
    #     return redirect('/')
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']

    #     user = authenticate(email=email, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('/home')
    #     else:
    #         messages.info(request, ("Invalid credentials "+email+"   "+password))
    #         return redirect('/login')

    # else:
    #     return render(request, 'AgentSignUp/signin_page.html')
        
def AgentSignUp(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        #agent = User()
        username = response.POST.get('username')
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
                agent=User.objects.create_Agent(username=username,full_name=full_name,email=email,password=password,city=city,Mobile=Mobile)
                agent.save()
                return redirect("/home")
            else:
                return render(response, "AgentSignUp/signup_page.html", {})
        elif password != pass2:
            return render(response, "AgentSignUp/signup_page.html", {})
            
    else:
        form = CreateNewAgent()
    return render(response, "AgentSignUp/signup_page.html", {"form":form})

def home(response):
    return render(response, "home.html", {})

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
            login(response, admin)
            messages.success(response, "Sign in successfully!")
            return redirect("/admin_homepage") 
    else:
        return render(response, "AdminSignIn/admin_signin.html", {})

@login_required
def AdminHomePage(request):
    # Id = request.user.
    # admin = User.objects.get(email=Id)
    # if admin.is_Admin ==True:
    username=request.user.username
    is_Admin=request.user.is_Admin
    #User.objects.get()
    if is_Admin:
        return render(request, "AdminHomePage/admin_homepage.html", {"username":username})
    return redirect("/home") 
    # return redirect("/home")


@login_required
def Logout(request):
    logout(request)
    return redirect('/home')

@login_required
def AgentRequestsList(request):
    agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    # if request.method == "POST":
    #     #agentID=request.POST.get("confirm")
    #     agent1ID=request.POST.get("confirm")
    #     if agent1ID is not None:
    #         User.objects.filter(ID=agent1ID).update(isConfirmedAgent=True)
    #         agent=User.objects.get(ID=agent1ID)        #email
    #         email=agent.email
    #         send_mail(
    #             'Your Request!',
    #             'Hello,Your request from StockFlow.com for Agent Account was confirmed,please enter the site to see the changes.Have A nice day:)',
    #             settings.DEFAULT_FROM_EMAIL,
    #             [email],
    #             fail_silently=False,
    #         )
    #         agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    #     else:
    #         agentID=request.POST.get("decline")
    #         if agentID is not None:
    #             agent=User.objects.get(ID=agentID)        # #email
    #             email=agent.email
    #             send_mail(
    #                 'Your Request!',
    #                 'Hello,Your request from StockFlow.com for Agent Account was declined.Have A nice day:)',
    #                 settings.DEFAULT_FROM_EMAIL,
    #                 [email],
    #                 fail_silently=False,
    #             )
    #             User.objects.filter(ID=agentID).delete()
    return render(request, "AdminHomePage/admin_agentrequestslist.html", {"agents":agents})

def agent_confirm(request):
    agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    if request.method == "POST":
        #agentID=request.POST.get("confirm")
        agent1ID=request.POST.get("confirm")
        if agent1ID is not None:
            User.objects.filter(ID=agent1ID).update(isConfirmedAgent=True)
            agent=User.objects.get(ID=agent1ID)        #email
            email=agent.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for Agent Account was confirmed,please enter the site to see the changes.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    return render(request, "AdminHomePage/admin_agentrequestslist.html", {"agents":agents})

@login_required
def Agent_Decline(request):
    agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    if request.method == "POST":
        agentID=request.POST.get("decline")
        if agentID is not None:
            agent=User.objects.get(ID=agentID)        # #email
            email=agent.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for Agent Account was declined.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            User.objects.filter(ID=agentID).delete()
    return render(request, "AdminHomePage/admin_agentrequestslist.html", {"agents":agents})
