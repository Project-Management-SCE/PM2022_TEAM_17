   
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
from accounts.models import User,Portfolios
from stocks.models import StockDeal
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

import yfinance as yf
import matplotlib.pyplot as plt
import io
import urllib, base64

from pandas_datareader import data
import pandas as pd



@login_required
def buyStock(request):
    if request.method == "POST":
        try:
            stockName = request.POST.get('stockName')
            stockAmount = request.POST.get('stockAmount')
            userID = request.user
            
            if (StockDeal.objects.filter(custID=userID).filter(stock=stockName)):
                Deal = StockDeal.objects.get(custID=userID,stock=stockName)
                Deal.isBuy = Deal.isBuy + int(stockAmount)
            else:       
                Deal = StockDeal(stock=stockName,custID=userID,isBuy=int(stockAmount))
            Deal.save()
            return render(request, "CustomerHomePage/customer_homepage.html", {})
        except:
            
            messages.error(request, f"Could not buy stock {request.POST.get('stockName')}")
            return render(request, "CustomerHomePage/customer_homepage.html", {})

def SearchStock(response):
    if response.method == "POST":
        try:
            plt.clf()
            stockTicker = response.POST.get('searchStock')
            stock = yf.Ticker(stockTicker)
            stockData = stock.history(period="4y")
            if 'Empty DataFrame' in str(stockData):
                raise Exception('Empty DataFrame - might be caused by an invalid symbol')
            stockData['Close'].plot(title=f"{stockTicker} stock price (in USD)")
            graph = plt.gcf()
            buf = io.BytesIO()
            graph.savefig(buf,format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            price = stock.info['regularMarketPrice']
            recom = stock.info['recommendationKey']
            website = stock.info['website']
            return render(response, "stock_view.html", {"price": price, "ticker": stockTicker, "recom": recom, "website": website, "graph": uri}, status=302)
        except Exception as e:
            print(e)
            messages.error(response, f"Stock named {stockTicker} doesn't found or not exists")
            if response.user.is_Customer:
                return redirect('/customer_homepage')
            elif response.user.is_Agent:
                return redirect('/agent_homepage')
            elif response.user.is_Admin:
                return redirect('/admin_homepage')
    else:
        if response.user.is_Customer:
            return redirect('/customer_homepage')
        elif response.user.is_Agent:
            return redirect('/agent_homepage')
        elif response.user.is_Admin:
            return redirect('/admin_homepage')
                
        


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
            if agent.isConfirmedAgent:
                login(response, agent)
                messages.success(response, "Sign in successfully!")
                agent.is_active = True
                agent.save()
                return redirect('/agent_homepage')
            else:
                messages.error(response, "Your account is not approved yet!")
                return render(response, "AgentSignUp/signin_page.html", {})
    else:
        return render(response, "AgentSignUp/signin_page.html", {})
        
def AgentSignUp(response):
    if(response.user.is_authenticated):
        return redirect('/')
    if response.method == "POST":
        username = response.POST.get('username')
        full_name = response.POST.get('full_name')
        email = response.POST.get('email')
        password = response.POST.get('password')
        pass2 = response.POST.get('password2')
        city = response.POST.get('city')
        Mobile = response.POST.get('Mobile')
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
            
    return render(response, "AgentSignUp/signup_page.html", {})

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
    username=request.user.username
    is_Admin=request.user.is_Admin
    if is_Admin:
        return render(request, "AdminHomePage/admin_homepage.html", {"username":username})
    return redirect("/home") 

@login_required
def AgentHomePage(request):
    username=request.user.username
    is_Agent=request.user.is_Agent
    isConfirmedAgent=request.user.isConfirmedAgent
    if is_Agent:
        return render(request, "AgentHomePage/agent_homepage.html", {"username":username,"isConfirmedAgent":isConfirmedAgent})
    return redirect("/home") 

@login_required
def CustomerHomePage(request):
    username=request.user.username
    is_Customer=request.user.is_Customer
    if is_Customer:
        return render(request, "CustomerHomePage/customer_homepage.html", {"username":username})
    return redirect("/home") 


@login_required
def Logout(request):
    logout(request)
    return redirect('/home')

@login_required
def AgentRequestsList(request):
    agents = User.objects.filter(isConfirmedAgent=False).filter(is_Agent=True)
    if request.method == "POST":
        if 'confirm' in request.POST:
            agent_confirm(request)
        if 'decline' in request.POST:
            Agent_Decline(request)
    return render(request, "AdminHomePage/admin_agentrequestslist.html", {"agents":agents})

def agent_confirm(request):
    if request.method == "POST":
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
                fail_silently=True,
            )
            return redirect('/admin_homepage')
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
                fail_silently=True,
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
def Customer_MyPortfolio(request):
    if request.user.is_Customer and not request.user.is_Agent:

        if request.method == "POST":
            if 'remove' in request.POST:
                StockDeal.objects.filter(custID_id=request.user.ID).delete()
                User.objects.filter(ID=request.user.ID).update(isPortfolio='None')
                return redirect('/customer_profile')
            elif 'sell' in request.POST:
                stockID=request.POST.get('sell')
                sell_Amount = request.POST.get('Sell_Amount')
                sd=StockDeal.objects.get(custID_id=request.user.ID,id=stockID)
                if (sd.isSell+int(sell_Amount))<=sd.amount: 
                    sd.isSell=sd.isSell+int(sell_Amount)
                    sd.save()
                else:
                    sd.isSell=sd.amount
                    sd.save()
            elif 'buy' in request.POST:
                stockID=request.POST.get('buy')
                buy_Amount = request.POST.get('Buy_Amount')
                sd=StockDeal.objects.get(custID_id=request.user.ID,id=stockID)
                sd.isBuy=sd.isBuy+int(buy_Amount)
                sd.save()
            
        if request.user.isPortfolio=="confirmed":

            stocks = StockDeal.objects.filter(custID_id=request.user.ID)
            
            tickers = [s.stock for s in stocks]
            amount = [s.amount for s in stocks]
            ids = [s.id for s in stocks]

            start_date = '2022-04-03'
            end_date = '2022-05-03'

            value = []
            for t in range(len(tickers)):
                panel_data = data.DataReader(str(tickers[t]), 'yahoo', start_date, end_date)
                price = panel_data['Close'][len(panel_data['Close'])-1]
                value.append(round(float(price*amount[t]), 2))

            d = []
            for i in range(len(tickers)):
                d.append((ids[i], tickers[i], amount[i], value[i]))

            pval = round(sum(value),2)

            return render(request, "Customer_Profile/customer_myportfolio.html", {"d": d, "pval": pval})

        else:
            return redirect('/customer_profile')
    else:

        return redirect('/home')


@login_required
def Agent_PortfolioRequests(request):
    if request.user.is_Agent and not  request.user.is_Customer:
        customers = User.objects.filter(isPortfolio="waiting").filter(is_Customer=True)
        agentID=request.user.ID
        if request.method == "POST":
            if 'confirm' in request.POST:
                portfolio_confirm(request,agentID)
            if 'decline' in request.POST:
                portfolio_decline(request)
        return render(request, "AgentHomePage/agent_portfoliorequests.html", {"customers":customers})
    else:
        return redirect('/home')


@login_required
def AgentActiveCustomers(request):
    if request.user.is_Agent and not request.user.is_Customer:

        agentid=request.user.ID
        cus = Portfolios.objects.filter(agentID=agentid)
        s=[]
        for c in cus:
            d=User.objects.get(ID=c.customerID)
            s.append(d)

        return render(request, "AgentHomePage/agent_active_customers.html", {"s":s})
    else:
        return redirect('/home')


def portfolio_decline(request):
    customers = User.objects.filter(isPortfolio="waiting").filter(is_Customer=True)
    if request.method == "POST":
        custID=request.POST.get("decline")
        if custID is not None:
            agent=User.objects.get(ID=custID)        # #email
            User.objects.filter(ID=custID).update(isPortfolio="None")
            email=agent.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for Portfolio was declined,You can try again.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
    return render(request, "AgentHomePage/agent_portfoliorequests.html", {"customers":customers})


def portfolio_confirm(request,agentID):
    customers = User.objects.filter(isPortfolio="waiting").filter(is_Customer=True)
    if request.method == "POST":
        customerID=request.POST.get("confirm")
        if customerID is not None:
            User.objects.filter(ID=customerID).update(isPortfolio="confirmed")
            cust=User.objects.get(ID=customerID)        #email
            email=cust.email
            send_mail(
                'Your Request For Portfolio!',
                'Hello,Your request from StockFlow.com for Portfolio was confirmed,please enter the site to see the changes.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            p=Portfolios(agentID=agentID,customerID=customerID)
            p.save()
        return render(request, "AgentHomePage/agent_portfoliorequests.html", {"customers":customers})
    return redirect('/home')

@login_required
def Agent_StockDeal(request):
    deals = StockDeal.objects.all()
    if request.method == "POST":
        if 'confirm_buy' in request.POST:
            buying_stock_confirm(request)
        if 'decline_buy' in request.POST:
            buying_stock_decline(request)
        if 'confirm_sell' in request.POST:
            sell_stock_confirm(request)
        if 'decline_sell' in request.POST:
            sell_stock_decline(request)
    return render(request, "AgentStocks/agent_stocks.html", {'Deals':deals})

def sell_stock_decline(request):
    deals = StockDeal.objects.all()
    if request.method == "POST":
        stockname=request.POST.get("stockname")
        customerID=request.POST.get("decline_sell")
        if customerID is not None:
            stock=StockDeal.objects.get(custID=int(customerID),stock=stockname)
            stock.isSell=0
            stock.save()
            customer=User.objects.get(ID=customerID)        #email
            email=customer.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for selling the stock '+stock.stock+' was declined.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            if(stock.amount==0 and stock.isBuy==0 ):
                stock.delete()
    return render(request, "AgentStocks/agent_stocks.html", {'Deals':deals})

def sell_stock_confirm(request):
    deals = StockDeal.objects.all()
    if request.method == "POST":
        customerID=request.POST.get("confirm_sell")
        stockname=request.POST.get("stockname")
        if customerID is not None:
            stock=StockDeal.objects.get(custID=int(customerID),stock=stockname)
            stock.amount=stock.amount-stock.isSell
            stock.isSell=0
            stock.save()
            if stock.amount==0 and stock.isBuy==0:
                stock.delete()
            customer=User.objects.get(ID=customerID)        #email
            email=customer.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for Selling the stock '+stock.stock+' was confirmed,please enter the site to see the changes.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            return render(request, "AgentStocks/agent_stocks.html", {'Deals':deals})
    return redirect('/home')

def buying_stock_confirm(request):
    deals = StockDeal.objects.all()
    if request.method == "POST":
        customerID=request.POST.get("confirm_buy")
        stockname=request.POST.get("stockname")
        if customerID is not None:
            stock=StockDeal.objects.get(custID=int(customerID),stock=stockname)
            stock.amount=stock.amount+stock.isBuy
            stock.isBuy=0
            stock.save()
            customer=User.objects.get(ID=customerID)        #email
            email=customer.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for Buying the stock '+stock.stock+' was confirmed,please enter the site to see the changes.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            return render(request, "AgentStocks/agent_stocks.html", {'Deals':deals})
    return redirect('/home')

def buying_stock_decline(request):
    deals = StockDeal.objects.all()
    if request.method == "POST":
        stockname=request.POST.get("stockname")
        customerID=request.POST.get("decline_buy")
        if customerID is not None:
            stock=StockDeal.objects.get(custID=int(customerID),stock=stockname)
            stock.isBuy=0
            stock.save()
            customer=User.objects.get(ID=customerID)        #email
            email=customer.email
            send_mail(
                'Your Request!',
                'Hello,Your request from StockFlow.com for Buying the stock '+stock.stock+' was declined.Have A nice day:)',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            if(stock.amount==0 and stock.isSell==0 ):
                stock.delete()
    return render(request, "AgentStocks/agent_stocks.html", {'Deals':deals})

def StockQuery(request):
    deals = StockDeal.objects.all()
    tickers=[]
    stocks=[]
    for stock in deals:
        if stocks is None:
            stocks.append((stock.stock,stock.amount))
            tickers.append(stock.stock)
        else:
            if stock.stock in tickers:
                for a in stocks:
                    if a[0]==stock.stock:
                        stocks.append((stock.stock,a[1]+stock.amount))
                        stocks.remove(a)
                        break
            else:
                stocks.append((stock.stock,stock.amount))
                tickers.append(stock.stock)
    return render(request, "AdminHomePage/admin_stockquery.html", {'stocks':stocks})

@login_required
def AgentQuery(request):
    sort = request.POST.get("sortBy")
    agents = User.objects.all().filter(is_Agent=True,isConfirmedAgent=True)
    AgentCust = {}
    for agent in agents:
        AgentCust[agent] = 0
    portfolios = Portfolios.objects.all()
    for p in portfolios:
        for agent in agents:
            if agent.ID == p.agentID:
                AgentCust[agent] += 1
    if sort == 'ID':
        AgentCust = {cust : agent for cust, agent in sorted(AgentCust.items(), key= lambda p: p[0].ID, reverse=True)}
    elif sort == 'Name':
        AgentCust = {cust : agent for cust, agent in sorted(AgentCust.items(), key= lambda p: p[0].full_name)}
    elif sort == 'Cust':
        AgentCust = {cust : agent for cust, agent in sorted(AgentCust.items(), key= lambda p: p[1], reverse=True)}
    return render(request, "AdminHomePage/admin_agentquery.html", {'agents':AgentCust})
    
