from django.urls import path
from . import views
from django.contrib import admin


app_name = 'AgentSignUp'
urlpatterns = [
    path("", views.home, name="index"),
    path("home/", views.home, name="home"),
    path("agent_signup/", views.AgentSignUp, name="agent_signup"),
    path('agent_signin/', views.AgentSignIn, name='agent_signin'),
    path("cust_signin/", views.CustomerSignIn, name="cust_signin"),
    path("cust_signup/", views.CustomerSignUp, name="cust_signup"),
    path("admin_signin/", views.AdminSignIn, name="admin_signin"),

    path("admin_homepage/", views.AdminHomePage, name="admin_homepage"),
    path("agent_homepage/", views.AgentHomePage, name="agent_homepage"),
    path("customer_homepage/", views.CustomerHomePage, name="customer_homepage"),

    path("logout", views.Logout, name="logout"),
    path("admin_agentrequestslist/", views.AgentRequestsList, name="admin_agentrequestslist"),

    path("admin_homepage/search_stock", views.SearchStock, name="Search_Stock1"),
    path("agent_homepage/search_stock", views.SearchStock, name="Search_Stock2"),
    path("customer_homepage/search_stock", views.SearchStock, name="Search_Stock3"),
    path("customer_homepage/buy_stock", views.buyStock, name="Buy_Stock"),
    path("customer_profile", views.Customer_Profile, name="Customer Profile"),
    path("agent_portfolio_requests", views.Agent_PortfolioRequests, name="Agent Profile"),
    path("agent_stock_deal", views.Agent_StockDeal, name="Agent Stock Deals"),
    #path("customer_buy", views.Customer_Purchase, name="Customer Stock Buy"),

]