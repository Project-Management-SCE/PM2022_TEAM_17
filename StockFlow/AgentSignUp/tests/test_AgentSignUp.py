from django.test import TestCase
from django.urls import reverse

class BaseTest(TestCase):
    def setUp(self):
        self.registerCustomer_url = reverse('cust_signup')
        self.registerAgent_url = reverse('agent_signup')
        self.loginCustomer_url = reverse('cust_signin')
        self.loginAgent_url = reverse('agent_signin')
        self.registerUser = {
            'full_name' : 'Test Testing',
            'email' : 'testemail@test.test',
            'city' : 'testcity',
            'Mobile' : '1234567890',
            'password' : 'testpass',
            'password2' : 'testpass'
        }

        self.loginUser = {
            'email' : 'testemail@test.test',
            'password' : 'testpass'
        }
        return super().setUp()


class AgentSignUpTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.registerAgent_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AgentSignUp/signup_page.html','base.html')

    def test_can_sign_up(self):
        response = self.client.post(self.registerAgent_url, self.registerUser, format='text/html')
        self.assertEqual(response.status_code,302)

class AgentSignInTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.loginAgent_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AgentSignUp/signin_page.html','base.html')
    
    def test_can_sign_in(self):
        response = self.client.post(self.loginAgent_url, self.loginUser, format='text/html')
        self.assertEqual(response.status_code,302)

class CustomerSignUpTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.registerCustomer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CustomerSignUp/signup_page.html','base.html')

    def test_can_sign_up(self):
        response = self.client.post(self.registerCustomer_url, self.registerUser, format='text/html')
        self.assertEqual(response.status_code,302)

class CustomerSignInTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.loginCustomer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CustomerSignUp/signin_page.html','base.html')

    def test_can_sign_in(self):
        response = self.client.post(self.loginCustomer_url, self.loginUser, format='text/html')
        self.assertEqual(response.status_code,302)