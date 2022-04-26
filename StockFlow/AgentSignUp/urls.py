from django.urls import path

from . import views

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
    path("logout", views.Logout, name="logout"),
    path("admin_agentrequestslist/", views.AgentRequestsList, name="admin_agentrequestslist"),
]
