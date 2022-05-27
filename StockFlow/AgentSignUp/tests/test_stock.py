from django.test import TestCase, Client
from accounts.models import User
from django.urls import reverse
import unittest

class TestAgentStock(TestCase):

    def setUp(self):
        self.agent = User.objects.create_Agent('testAgentUserName','testAgentName','testAgentEmail@test.com','testAgentPass','testAgentCity','Agent1234567890')


    def test_Agent_stock(self):
        response = self.client.post(reverse('AgentSignUp:Search_Stock_agent'), data={
            'searchStock':'MSFT'})
        self.assertEqual(response.status_code,302) 

    def test_Agent_wrong_stock(self):
        self.assertRaises(Exception,self.client.post('AgentSignUp:Search_Stock_agent', data={
            'searchStock':'badStock'}))




class TestAdminStock(TestCase):

    def setUp(self):
        self.admin = User.objects.create_Admin('testAdminUserName','testAdminName','testAdminEmail@test.com','testAdminPass')


    def test_Admin_stock(self):
        response = self.client.post(reverse('AgentSignUp:Search_Stock_admin'), data={
            'searchStock':'MSFT'})
        self.assertEqual(response.status_code,302) 

    
    def test_Admin_wrong_stock(self):
        self.assertRaises(Exception,self.client.post('AgentSignUp:Search_Stock_admin', data={
            'searchStock':'badStock'}))
        




class TestCustomerStock(TestCase):

    def setUp(self):
        self.customer = User.objects.create_Customer('testCustomerUserName','testCustomerName','testCustomerEmail@test.com','testCustomerPass','testCustomerCity','Customer1234567890')


    def test_Customer_stock(self):
        response = self.client.post(reverse('AgentSignUp:Search_Stock_cust'), data={
            'searchStock':'MSFT'})
        self.assertEqual(response.status_code,302) 

    
    def test_Customer_wrong_stock(self):
        self.assertRaises(Exception,self.client.post('AgentSignUp:Search_Stock_cust', data={
            'searchStock':'badStock'}))
        

