from django.db import models
from accounts.models import User
# Create your models here.

class StockDeal(models.Model):
    custID = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.CharField(max_length=50)
    isSell = models.IntegerField(default=0)
    isBuy = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)    

    def __str__(self):
        return f'{self.custID},{self.stock},{self.amount}' 
    
