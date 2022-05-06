   
import time
from email import message
from re import A

from typing import List
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from matplotlib.pyplot import get
from requests import request

from accounts.models import WAIT
#from requests import request
from .forms import CreateNewAgent
from django.contrib import messages
# Create your views here.
from accounts.models import User
from stocks.models import StockDeal
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

import yfinance as yf

@login_required
#def Customer_Purchase(request):
#    tickers = ['AAPL', 'MSFT', 'AMD', 'SPY', 'LYFT', 'SOS', 'ATVI', 'RDBX', '^TNX', 'BRK-B', 'FRGE'][0:3]
#    stocks = {}
#    for s in tickers:
#        tickerInfo = yf.Ticker(s).info
#        stocks[s] = {'name': tickerInfo['shortName'], 'price':tickerInfo['regularMarketPrice']}
#    return render(request,"CustomerStockBuy/customer_buy.html",{'stocks': stocks})

@login_required
def buyStock(request):
    if request.method == "POST":
        try:
            stockName = request.POST.get('stockName')
            stockAmount = request.POST.get('stockAmount')
            userID = request.user
            Deal = StockDeal(stock=stockName,custID=userID,isBuy=stockAmount)
            if (StockDeal.objects.filter(custID=userID)):
                customer = StockDeal.objects.filter(custID=userID)
                Deal.amount = customer.amount
                Deal.isSell = customer.isSell
            Deal.save()
            return render(request, "CustomerHomePage/customer_homepage.html", {})
        except:
            messages.error(request, f"Could not buy stock {request.POST.get('stockName')}")
            return render(request, "CustomerHomePage/customer_homepage.html", {})

def SearchStock(response):
    if response.method == "POST":
        try:
            searchStock = response.POST.get('searchStock')
            stock = yf.Ticker(searchStock)
            price = stock.info['regularMarketPrice']
            symbol = stock.info['symbol']
            recom = stock.info['recommendationKey']
            website = stock.info['website']
            return render(response, "stock_view.html", {"price": price, "ticker": symbol, "recom": recom, "website": website})
        except:
            messages.error(response, f"Stock named {searchStock} doesn't found or not exists")
            return render(response, "CustomerHomePage/customer_homepage.html", {})
    
        


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
            return render(response, "CustomerSignUp/signin_page.html", {})
        if cust is not None:    
            login(response, cust)
            cust.is_active = True
            cust.save()
            messages.success(response,"Sign in successfully!")
            return redirect('/customer_homepage')
            #return render(response, "AgentSignUp/home.html", {})
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
    # if(response.user.is_authenticated):
    #     return redirect('/')
    if response.method == "POST":
        emailCheck = response.POST.get('email')
        passwordCheck = response.POST.get('password')
        try:
            agent = User.objects.get(email = emailCheck,password = passwordCheck)
        except User.DoesNotExist: # if agent with such email or password doesn't exists or some of the data is wrong
            messages.error(response, "one or more of the credentials are incorrect!")
            return render(response, "AgentSignUp/signin_page.html", {})
        if agent is not None:
            login(response, agent)
            messages.success(response, "Sign in successfully!")
            agent.is_active = True
            agent.save()
            #return render(response, "AgentHomePage/agent_homepage.html", {})  
            #return AgentHomePage(response)
            #return render(response, "AgentHomePage/agent_homepage.html", {})
            return redirect("/agent_homepage")
            #return HttpResponse("<h1>No ticker exist<h1>")


    else:
        return render(response, "AgentSignUp/signin_page.html", {})

# def AdminSignIn(response):
#     if response.method == "POST":
#         emailCheck = response.POST.get('emailLogin')
#         passwordCheck = response.POST.get('passLogin')
#         try:
#             admin = User.objects.get(email = emailCheck,password = passwordCheck,is_Admin=True)
#         except User.DoesNotExist: # if agent with such email or password doesn't exists or some of the data is wrong
#             messages.error(response, "one or more of the credentials are incorrect!")
#             return render(response, "AdminSignIn/admin_signin.html", {})
#         if admin is not None:
#             login(response, admin)
#             messages.success(response, "Sign in successfully!")
#             return redirect("/admin_homepage") 
#     else:
#         return render(response, "AdminSignIn/admin_signin.html", {})

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
            return render(response, "AdminSignIn/admin_signin.html", {})
        if admin is not None:
            login(response, admin)
            messages.success(response, "Sign in successfully!")
            admin.is_active = True
            admin.save()
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
def AgentHomePage(request):
    # Id = request.user.
    # admin = User.objects.get(email=Id)
    # if admin.is_Admin ==True:
    username=request.user.username
    is_Agent=request.user.is_Agent
    #User.objects.get()
    if is_Agent:
        return render(request, "AgentHomePage/agent_homepage.html", {"username":username})
    return redirect("/home") 
    # return redirect("/home")

@login_required
def CustomerHomePage(request):
    # Id = request.user.
    # admin = User.objects.get(email=Id)
    # if admin.is_Admin ==True:
    username=request.user.username
    is_Customer=request.user.is_Customer
    #User.objects.get()
    if is_Customer:
        return render(request, "CustomerHomePage/customer_homepage.html", {"username":username})
    return redirect("/home") 
    # return redirect("/home")


@login_required
def Logout(request):
    logout(request)
    return redirect('/home')

@login_required
def AgentRequestsList(request):
    agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    if request.method == "POST":
        #agentID=request.POST.get("confirm")
        if 'confirm' in request.POST:
            agent_confirm(request)
        if 'decline' in request.POST:
            Agent_Decline(request)
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
            return redirect('/admin_homepage')
    #return render(request, "AdminHomePage/admin_agentrequestslist.html", {"agents":agents})
    return redirect('/home')


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

@login_required
def Customer_Profile(request):
    if request.user.is_Customer and not request.user.is_Agent:
        if request.method == "POST":
            request.user.isPortfolio = "waiting"
            request.user.save()
            return render(request, "Customer_Profile/customer_profilepage.html", {})
        else:
            return render(request, "Customer_Profile/customer_profilepage.html", {})
    else:
        return redirect('/home')


@login_required
def Agent_PortfolioRequests(request):
    if request.user.is_Agent and not  request.user.is_Customer:
        customers = User.objects.filter(isPortfolio="waiting").filter(is_Customer=True)
        return render(request, "AgentHomePage/agent_portfoliorequests.html", {"customers":customers})
    else:
        return redirect('/home')

@login_required
def Agent_StockDeal(request):
    deals = StockDeal.objects.all()
    return render(request, "AgentStocks/agent_stocks.html", {'Deals':deals})