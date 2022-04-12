from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("home/", views.home, name="home"),
    path("agent_signup/", views.AgentSignUp, name="agent_signup"),
    path("agent_signin/", views.AgentSignIn, name="agent_signin"),

]