from email import message
from re import A
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from requests import request
from .forms import CreateNewAgent
from .models import Agent
from django.contrib import messages
# Create your views here.

def AgentSignIn(response):
    if response.method == "POST":
        emailCheck = response.POST.get('emailLogin')
        passwordCheck = response.POST.get('passLogin')
        try:
            agentEmailCheck = Agent.objects.get(email = emailCheck)
            agentPassCheck = Agent.objects.get(password = passwordCheck)
        except Agent.DoesNotExist:
            return render(response, "AgentSignUp/signin_page.html", {'alert': True})
        return redirect("/home")
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
        if agent.password == pass2:
            if not agentEmailTest:
                agent.save()
                return redirect("/home")
            else:
                return render(response, "AgentSignUp/signup_page.html", {'alert_email': True})
        elif agent.password != pass2:
            return render(response, "AgentSignUp/signup_page.html", {'alert_pass': True})
            
    else:
        form = CreateNewAgent()
    return render(response, "AgentSignUp/signup_page.html", {"form":form})

def home(response):
    return render(response, "AgentSignUp/home.html", {})

