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

def CustomerSignIn(response):
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            custEmailCheck = Customer.objects.get(email = emailCheck)
            custPassCheck = Customer.objects.get(password = passwordCheck)
        except Customer.DoesNotExist: # if customer with such email or password doesn't exists or some of the data is wrong
            return render(response, "CustomerSignUp/signin_page.html", {'alert': True})
        return render(response, "CustomerSignUp/home.html", {'success': True})
    else:
        return render(response, "CustomerSignUp/signin_page.html", {})

def CustomerSignUp(response):
    if response.method == "POST":
        cust = Customer()
        cust.full_name = response.POST.get('full_name')
        cust.email = response.POST.get('email')
        cust.password = response.POST.get('password')
        pass2 = response.POST.get('password2')
        cust.city = response.POST.get('city')
        cust.Mobile = response.POST.get('Mobile')
        cust.isPortfolio = False
        try:
            custEmailTest = Customer.objects.get(email = cust.email)
        except Customer.DoesNotExist:
            custEmailTest = None
            return render(response, "CustomerSignUp/signup_page.html", {'alert_email': True})
        if cust.password == pass2:
            if not custEmailTest:
                cust.save()
                return redirect("/home")
            else:
                return render(response, "CustomerSignUp/signup_page.html", {'alert_email': True})
        elif cust.password != pass2:
            return render(response, "CustomerSignUp/signup_page.html", {'alert_pass': True})
    else:
        return render(response, "CustomerSignUp/signup_page.html", {})


def AgentSignIn(response):
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            agentEmailCheck = Agent.objects.get(email = emailCheck)
            agentPassCheck = Agent.objects.get(password = passwordCheck)
        except Agent.DoesNotExist: # if agent with such email or password doesn't exists or some of the data is wrong
            return render(response, "AgentSignUp/signin_page.html", {'alert': True})
        return render(response, "AgentSignUp/home.html", {'success': True})
    else:
        return render(response, "AgentSignUp/signin_page.html", {})
        
def AgentSignUp(response):
    if response.method == "POST":
        agent = Agent()
        agent.full_name = response.POST.get('full_name')
        agent.email = response.POST.get('email')
        agent.password = response.POST.get('password')
        pass2 = response.POST.get('password2')
        agent.city = response.POST.get('city')
        agent.Mobile = response.POST.get('Mobile')
        agent.isAgent = False
        try:
            agentEmailTest = Agent.objects.get(email = agent.email)
        except Agent.DoesNotExist:
            agentEmailTest=None 
            return render(response, "AgentSignUp/signup_page.html", {'alert_email': True})
        if agent.password == pass2:
            if not agentEmailTest:
                agent.save()
                return redirect("/home")
            else:
                return render(response, "AgentSignUp/signup_page.html", {'alert_email': True})
        elif agent.password != pass2:
            return render(response, "AgentSignUp/signup_page.html", {'alert_pass': True})
            
    else:
        return render(response, "AgentSignUp/signup_page.html", {})

def home(response):
    return render(response, "AgentSignUp/home.html", {})

