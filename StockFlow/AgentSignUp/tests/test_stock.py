from urllib import response
from django.test import TestCase, Client
from accounts.models import User
from stocks.models import StockDeal
from django.urls import reverse


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

    def test_empty_stock_query(self):
        response = self.client.get('/admin_stockquery/',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertFalse(response.context['stocks'])

    def test_stock_query(self):
        cust = User.objects.create_Customer('testCustomerUserName','testCustomerName','testCustomerEmail@test.com','testCustomerPass','testCustomerCity','Customer1234567890')
        cust.save()
        deal = StockDeal(custID=cust, stock='MSFT')
        deal.save()
        response = self.client.get('/admin_stockquery/',follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.context['stocks'])
        self.assertEqual(response.context['stocks'][0],('MSFT',0))

    
        




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
        

