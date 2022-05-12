from django.test import TestCase, Client
from accounts.models import User
from django.urls import reverse


class TestAgentStock(TestCase):

    def setUp(self):
        self.agent = User.objects.create_Agent('testAgentUserName','testAgentName','testAgentEmail@test.com','testAgentPass','testAgentCity','Agent1234567890')


    def test_Agent_stock(self):
        response = self.client.post(reverse('AgentSignUp:Search_Stock'), data={
            'searchStock':self.agent.get_searchStock()})
        self.assertEqual(response.status_code,302) # status code 302 is redirect method

    def test_Agent_wrong_stock(self):
        response = self.client.post(reverse('AgentSignUp:Search_Stock'), data={
            'searchStock':'wrongStock'})
        self.assertEqual(response.status_code,200) # status code 200 is render method




class TestAdminStock(TestCase):

    def setUp(self):
        self.admin = User.objects.create_Admin('testAdminUserName','testAdminName','testAdminEmail@test.com','testAdminPass','testAdminCity','Admin1234567890')


    def test_Admin_stock(self):
        response = self.client.post(reverse('AdminSignUp:Search_Stock'), data={
            'searchStock':self.admin.get_searchStock()})
        self.assertEqual(response.status_code,302) # status code 302 is redirect method

    def test_Admin_wrong_stock(self):
        response = self.client.post(reverse('AdminSignUp:Search_Stock'), data={
            'searchStock':'wrongStock'})
        self.assertEqual(response.status_code,200) # status code 200 is render method




class TestCustomerStock(TestCase):

    def setUp(self):
        self.customer = User.objects.create_Customer('testCustomerUserName','testCustomerName','testCustomerEmail@test.com','testCustomerPass','testCustomerCity','Customer1234567890')


    def test_Customer_stock(self):
        response = self.client.post(reverse('CustomerSignUp:Search_Stock'), data={
            'searchStock':self.customer.get_searchStock()})
        self.assertEqual(response.status_code,302) # status code 302 is redirect method

    def test_Customer_wrong_stock(self):
        response = self.client.post(reverse('CustomerSignUp:Search_Stock'), data={
            'searchStock':'wrongStock'})
        self.assertEqual(response.status_code,200) # status code 200 is render method

