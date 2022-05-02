from django.test import TestCase, Client
from accounts.models import User
from django.urls import reverse


class TestAgentUser(TestCase):


    def setUp(self):
       self.agent = User.objects.create_Agent('testAgentUserName','testAgentName','testAgentEmail@test.com','testAgentPass','testAgentCity','Agent1234567890')
       

    def test_Agent_exist(self):
        self.assertTrue(self.agent)
        self.assertEqual('testAgentName',self.agent.get_full_name())
        self.assertEqual('testAgentEmail@test.com',self.agent.get_email())

    def test_user_is_agent(self):
        self.assertFalse(self.agent.is_Customer)
        self.assertFalse(self.agent.is_Admin)
        self.assertTrue(self.agent.is_Agent)

    def test_Agent_signup_url(self):
        response = self.client.get("/agent_signup/")
        self.assertEqual(response.status_code,200) # status code 200 is render method
        self.assertTemplateUsed(response,'AgentSignUp/signup_page.html')

    def test_Agent_signup_form(self):
        response = self.client.post(reverse('AgentSignUp:agent_signup'), data={
            'email': self.agent.get_email(),
            'full_name': self.agent.get_full_name(),
            'city' : self.agent.get_city(),
            'password': self.agent.get_password(),
            'Mobile' : self.agent.get_mobile()
        })
        self.assertEqual(response.status_code,200) # status code 200 is render method
        users = User.objects.all()
        self.assertEqual(users.count(), 1)


    def test_Agent_signin_url(self):
        response = self.client.get("/agent_signin/")
        self.assertEqual(response.status_code,200) # status code 200 is render method
        self.assertTemplateUsed(response,'AgentSignUp/signin_page.html')

    def test_Agent_signin_form(self):
        response = self.client.post(reverse('AgentSignUp:agent_signin'), data={
            'email':self.agent.get_email(),
            'password':self.agent.get_password()})
        self.assertEqual(response.status_code,302) # status code 302 is redirect method

    def test_wrong_Agent_signin_form(self):
        response = self.client.post(reverse('AgentSignUp:agent_signin'), data={
            'email':'wrongEmail@test.com',
            'password':'wrongPass'})
        self.assertEqual(response.status_code,200) # status code 200 is render method
    

class TestCustomerUser(TestCase):
    def setUp(self):
        self.data = {
            'username':'testCustUserName',
            'full_name':'testCustName',
            'email':'testCustEmail@test.com',
            'password':'testCustPass',
            'city':'testCustCity',
            'Mobile':'Cust1234567890'
        }
        self.customer = User.objects.create_Customer(self.data['username'],self.data['full_name'],self.data['email'],self.data['password'],self.data['city'],self.data['Mobile'])

    def test_Customer_exists(self):
        self.assertTrue(self.customer)
        self.assertEqual('testCustName',self.customer.get_full_name())
        self.assertEqual('testCustEmail@test.com',self.customer.get_email())

    def test_user_is_customer(self):
        self.assertFalse(self.customer.is_Admin)
        self.assertFalse(self.customer.is_Agent)
        self.assertTrue(self.customer.is_Customer)
        
    def test_Customer_signup_url(self):
        response = self.client.get("/cust_signup/")
        self.assertEqual(response.status_code,200) # status code 200 is render method
        self.assertTemplateUsed(response,'CustomerSignUp/signup_page.html')

    def test_Customer_signup_form(self):
        response = self.client.post(reverse('AgentSignUp:cust_signup'), data={
            'email': self.customer.get_email(),
            'full_name': self.customer.get_full_name(),
            'city' : self.customer.get_city(),
            'password': self.customer.get_password(),
            'Mobile' : self.customer.get_mobile()
        })
        self.assertEqual(response.status_code,200) # status code 200 is render method
        users = User.objects.all()
        self.assertEqual(users.count(), 1)


    def test_Customer_signin_url(self):
        response = self.client.get("/cust_signin/")
        self.assertEqual(response.status_code,200) # status code 200 is render method
        self.assertTemplateUsed(response,'CustomerSignUp/signin_page.html')

    def test_Customer_signin_form(self):
        response = self.client.post(reverse('AgentSignUp:cust_signin'), data={
            'emailLogin':self.customer.get_email(),
            'passLogin':self.customer.get_password()})
        self.assertEqual(response.status_code,302) # status code 302 is redirect method
    
    def test_wrong_Customer_signin_form(self):
        response = self.client.post(reverse('AgentSignUp:cust_signin'), data={
            'emailLogin':'wrongEmail@test.com',
            'passLogin':'wrongPass'})
        self.assertEqual(response.status_code,200) # status code 200 is render method



class TestAdminUser(TestCase):
    def setUp(self):
        self.admin = User.objects.create_Admin('testAdminUserName','testAdminEmail@test.com','testAdminName','testAdminPass')


    def test_admin_exists(self):
        self.assertTrue(self.admin)
        self.assertEqual('testAdminEmail@test.com', self.admin.get_email())
        self.assertEqual('testAdminName', self.admin.get_full_name())
        self.assertEqual('testAdminPass', self.admin.get_password())

    def test_user_is_admin(self):
        self.assertFalse(self.admin.is_Customer)
        self.assertFalse(self.admin.is_Agent)
        self.assertTrue(self.admin.is_Admin)
    
    def test_admin_signin_url(self):
        response = self.client.get("/admin_signin/")
        self.assertEqual(response.status_code,200) # status code 200 is render method
        self.assertTemplateUsed(response,'AdminSignIn/admin_signin.html')

    def test_admin_signin_form(self):
        response = self.client.post(reverse('AgentSignUp:admin_signin'), data={
            'emailLogin':self.admin.get_email(),
            'passLogin':self.admin.get_password()})
        self.assertEqual(response.status_code,302) # status code 302 is redirect method

    def test_wrong_Admin_signin_form(self):
        response = self.client.post(reverse('AgentSignUp:admin_signin'), data={
            'emailLogin':'wrongEmail@test.com',
            'passLogin':'wrongPass'})
        self.assertEqual(response.status_code,200) # status code 200 is render method
