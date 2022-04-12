
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
WAIT="waiting"
CON="confirmed"
DEC="declined"
NON="None"
PORTFOLIO_CHOICES=((WAIT,"waiting"),(CON,"confirmed"),(DEC,"declined"),(NON,"None"))

class MyAccManager(BaseUserManager):
    def create_Customer(self,full_name,email,password,city,Mobile):
        if not email:
            raise ValueError("Users must have an email address")
        if not full_name:
            raise ValueError("Users must have an full name")
        customer = self.model(
            full_name = full_name,
            email=self.normalize_email(email),
            city=city,
            Mobile=Mobile,
            password=password,
            is_Customer=True,
        ) 
        customer.save(using=self._db)
        return customer

    def create_Agent(self,full_name,email,password,city,Mobile):
        if not email:
            raise ValueError("Users must have an email address")
        if not full_name:
            raise ValueError("Users must have an full name")
        agent = self.model(
            full_name = full_name,
            email=self.normalize_email(email),
            city=city,
            Mobile=Mobile,
            password=password,
            is_Agent=True,
           
        )
        agent.save(using=self._db)
        return agent

    def create_Admin(self,email,full_name,password):
        admin = self.model(
            full_name = full_name,
            email=self.normalize_email(email),
            password=password,
            is_Admin=True,
        )
        admin.save(using=self._db)
        return admin

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    ID= models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    is_Customer = models.BooleanField(default=False)
    is_Agent = models.BooleanField(default=False) 
    is_Admin = models.BooleanField(default=False) 

    full_name = models.CharField(max_length=80)
    city = models.CharField(max_length=50)
    Mobile = models.CharField(max_length=10)
    
    isConfirmedAgent = models.BooleanField(default=False)#if Agent is already got confirmation from Admin

    isPortfolio=models.CharField(max_length=10,choices=PORTFOLIO_CHOICES,default="None")#if Customer is requesting,waiting or got declined for portfolio
    # notice the absence of a "Password field", that is built in.

    objects = MyAccManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_email(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_customer(self):
        "Is the user a member of staff?"
        return self.is_Customer

    @property
    def is_agent(self):
        "Is the user a admin member?"
        return self.is_Agent

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.is_Admin