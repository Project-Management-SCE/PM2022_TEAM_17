from django.test import TestCase, Client
from accounts.models import User
from stocks.models import StockDeal
from django.urls import reverse

customerData = {
            'username':'IntegCustomer',
            'full_name':'IntegCustomer',
            'email':'IntegCustomer@test.com',
            'password':'123123',
            'password2':'123123',
            'city':'IntegCity',
            'Mobile':'0541234567'
        }

agentData = {
            'username':'IntegAgent',
            'full_name':'IntegAgent',
            'email':'IntegAgent@test.com',
            'password':'123123',
            'password2':'123123',
            'city':'IntegCity',
            'Mobile':'0541234567'
        }

adminData = {
            'username':'IntegAdmin',
            'full_name':'IntegAdmin',
            'email':'IntegAdmin@test.com',
            'password':'123123',
            'city':'IntegCity',
            'Mobile':'0541234567'
    }

class TestCustomer(TestCase):

    def test_Customer(self): # Sign up =>  Sign in => Search Stock => Buy Stock
        self.client.post('/cust_signup/', data=customerData) # Sign Up The Customer User
        response = self.client.post(reverse('AgentSignUp:cust_signin'),  # Sign In the Customer User
        data={'emailLogin': customerData['email'], 'passLogin':customerData['password']}, follow=True)

        message = list(response.context['messages'])[0]
        user = response.context['user']
        self.assertEqual(str(message),'Sign in successfully!')
        self.assertEqual(user.username,customerData['username'])
        stock = 'MSFT'
        stockAmount = 4
        self.client.post('/customer_homepage/', data={'searchStock': stock}) # Customer Search Stock MSFT
        response = self.client.post(reverse('AgentSignUp:Buy_Stock'), data={'stockName': stock, 'stockAmount': stockAmount}, follow=True)
    
    
    
     
        
class TestAgent(TestCase):

    def test_Agent(self): # Sign up =>  Sign in => Search Stock 
        admin = User.objects.create_Admin(adminData['username'],adminData['email'],adminData['full_name'],adminData['password'])
        admin.save() # creating admin for confirming agent
        
        self.client.post('/agent_signup/', data=agentData) # Sign Up The Agent User
        agent = User.objects.all().filter(username=agentData['username']) # getting the agent object for passing his id in the confirm button
        
        self.client.post('/admin_signin/',  # Sign in as Admin
        data={'emailLogin':adminData['email'], 'passLogin':adminData['password']}, follow=True)
        
        self.client.post('/admin_agentrequestslist/',data={'confirm':agent[0].ID},follow=True) # confirming agent as admin
        self.client.get('/logout') # logout as admin
        
        response = self.client.post(reverse('AgentSignUp:agent_signin'),  # Sign In the Agent User
        data={'email': agentData['email'], 'password':agentData['password']}, follow=True)
        
        message = list(response.context['messages'])[0]
        
        user = response.context['user']
        self.assertEqual(str(message),'Sign in successfully!')
        self.assertEqual(user.username,agentData['username'])
        stock = 'MSFT'
        self.client.post('/agent_homepage/', data={'searchStock': stock}) # Customer Search Stock MSFT
        
    
    def test_potfolio_confirm(self): # Agent Signup => Admin Signin => Admin Confirm Agent => Admin Logout =>
                                     # => Customer Signup => Customer Signin => Customer Portfolio Request =>
                                     # => Customer Logout => Agent Signin => Agent Confirm Portfolio Request.
        admin = User.objects.create_Admin(adminData['username'],adminData['email'],adminData['full_name'],adminData['password'])
        admin.save()
        self.client.post('/agent_signup/', data=agentData) # Sign Up The Agent User
        agent = User.objects.all().filter(username=agentData['username'])

        self.client.post('/admin_signin/',  # Sign in as Admin
        data={'emailLogin':adminData['email'], 'passLogin':adminData['password']})

        self.client.post('/admin_agentrequestslist/',data={'confirm':agent[0].ID}) # confirming agent as admin
        self.client.get('/logout') # logout as admin
        
        self.client.post('/cust_signup/', data=customerData) # Sign Up the Customer User
        customer = User.objects.all().filter(is_Customer=True)
        self.client.post(reverse('AgentSignUp:cust_signin'),  # Sign In the Customer User
        data={'emailLogin': customerData['email'], 'passLogin':customerData['password']}, follow=True)
        self.client.post('/customer_profile') # customer open request for portfolio

        self.assertEqual(customer[0].isPortfolio,"waiting","Should be waiting status after request and before confirmation")
        self.client.get('/logout') # logout as customer

        self.client.post(reverse('AgentSignUp:agent_signin'),  # Sign In the Agent User
        data={'email': agentData['email'], 'password':agentData['password']}, follow=True)
        self.client.post('/agent_portfolio_requests', data={'confirm':customer[0].ID}) # agent confirm customer portfolio request
        self.assertEqual(customer[0].isPortfolio,"confirmed","Should be confirmed status after confirmation")




        

    
'''   
    
'''

    




