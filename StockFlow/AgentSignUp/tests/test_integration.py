from distutils.sysconfig import customize_compiler
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
        
    def test_Customer(self): # Customer Sign up => Customer Sign in => 
                             # => Customer Search Stock => Customer Buy Stock
        self.client.post('/cust_signup/', data=customerData) # Sign Up The Customer User
        response = self.client.post(reverse('AgentSignUp:cust_signin'),  # Sign In the Customer User
        data={'emailLogin': customerData['email'], 'passLogin':customerData['password']}, follow=True)
        customer = User.objects.get(is_Customer=True)
        customer.isPortfolio = True
        message = list(response.context['messages'])[0]
        user = response.context['user']
        self.assertEqual(str(message),'Sign in successfully!')
        self.assertEqual(user.username,customerData['username'])
        stock = 'MSFT'
        stockAmount = 4
        self.client.post('/customer_homepage/', data={'searchStock': stock}) # Customer Search Stock MSFT
        response = self.client.post(reverse('AgentSignUp:Buy_Stock'), data={'stockName': stock, 'stockAmount': stockAmount}, follow=True)
    
    def test_Sell_from_Portfolio(self):  # Agent Signup => Admin Signin => Admin Confirm Agent => Admin Logout =>
                                         # => Customer Signup => Customer Signin => Customer Portfolio Request =>
                                         # => Customer Logout => Agent Signin => Agent Confirm Portfolio Request =>
                                         # => Agent Logout => Customer Signin => Customer Search Stock MSFT => 
                                         # => Customer Buy 4 Stock MSFT => Customer Logout => Agent Signin =>
                                         # => Agent Confirm Customer Buy => Agent Logout => Customer SignIn =>
                                         # => Customer Sell Stock via Portfolio Page
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

        self.client.get('/logout') # logout as customer

        self.client.post(reverse('AgentSignUp:agent_signin'),  # Sign In the Agent User
        data={'email': agentData['email'], 'password':agentData['password']}, follow=True)
        self.client.post('/agent_portfolio_requests', data={'confirm':customer[0].ID}) # agent confirm customer portfolio request
        
        self.client.get('/logout') # logout as agent

        self.client.post(reverse('AgentSignUp:cust_signin'),  # Sign In the Customer User
        data={'emailLogin': customerData['email'], 'passLogin':customerData['password']}, follow=True)

        stock = 'MSFT'
        stockAmount = 4
        self.client.post('/customer_homepage/', data={'searchStock': stock}) # Customer Search Stock MSFT
        self.client.post(reverse('AgentSignUp:Buy_Stock'), data={'stockName': stock, 'stockAmount': stockAmount}) # Customer Buy Stock
        #deal = StockDeal.objects.all()[0]
        #print(deal.id, deal.amount, deal.isBuy, deal.isSell)
        self.client.get('/logout') # logout as customer

        self.client.post(reverse('AgentSignUp:agent_signin'),  # Sign In the Agent User
        data={'email': agentData['email'], 'password':agentData['password']}, follow=True)

        self.client.post('/agent_stock_deal', {'confirm_buy':customer[0].ID,'stockname':stock}) # Agent Confirm Buy
        self.client.get('/logout') # logout as agent

        self.client.post(reverse('AgentSignUp:cust_signin'),  # Sign In the Customer User
        data={'emailLogin': customerData['email'], 'passLogin':customerData['password']}, follow=True)
        deal = StockDeal.objects.all()[0]
        self.assertTrue(deal)
        self.assertEqual(deal.amount, stockAmount)

        self.assertEqual(deal.isSell,0)
        self.client.post(reverse('AgentSignUp:Customer MyPortfolio'), {'sell':deal.id, 'Sell_Amount':'2'}, follow=True)
        deal = StockDeal.objects.all()[0]
        self.assertEqual(deal.amount, stockAmount)
        self.assertEqual(deal.isSell,2)

        

        
class TestAgent(TestCase):

    def test_Agent(self): # Agent Sign up => Admin Sign in => Admin Confirm Agent => 
                          # => Admin Logout => Agent Sign In => Search Stock 
        admin = User.objects.create_Admin(adminData['username'],adminData['email'],adminData['full_name'],adminData['password'])
        admin.save() # creating admin for confirming agent
        self.client.post('/agent_signup/', data=agentData) # Sign Up The Agent User
        agent = User.objects.all().filter(username=agentData['username']) # getting the agent object for passing his id in the confirm button
        self.assertEqual(agent[0].username,agentData['username'])
        response = self.client.post('/admin_signin/',  # Sign in as Admin
        data={'emailLogin':adminData['email'], 'passLogin':adminData['password']}, follow=True)
        self.assertEqual(response.context['user'].username,admin.username)
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
    
    def test_portfolio_decline(self): # Agent Signup => Admin Signin => Admin Confirm Agent => Admin Logout =>
                                      # => Customer Signup => Customer Signin => Customer Portfolio Request =>
                                      # => Customer Logout => Agent Signin => Agent Decline Portfolio Request.
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
        self.client.post('/agent_portfolio_requests', data={'decline':customer[0].ID}) # agent confirm customer portfolio request
        self.assertEqual(customer[0].isPortfolio,"None","Should be None status after confirmation")