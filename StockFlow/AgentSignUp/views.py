from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateNewAgent

# Create your views here.

def AgentSignUp(response):
    if response.method == "POST":
        form = CreateNewAgent(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = CreateNewAgent()

    return render(response, "AgentSignUp/signup_page.html", {"form":form})

def home(response):
    return render(response, "AgentSignUp/home.html", {})