from django.db import models
from django.contrib.auth.models import User

class StockActions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateTimeField(auto_now_add=True)
    # company_name = models.CharField(max_length=20,unique=False)
    
    # this are trade choices available for any stock
    TRADE_CHOICES = (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
        ("SPLIT", "SPLIT")
    )
    trade_type = models.CharField(max_length=20,
                                  choices=TRADE_CHOICES,
                                 blank=False)

    quantity = models.IntegerField(null=False,blank=False)
    price = models.FloatField(null=False,blank=False)
    

class SplitAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateTimeField(auto_now_add=True)
    ratio = models.FloatField(null=False,blank=False)
    

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    # company_name = models.CharField(max_length=100,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False,default=0)
    amount_invested = models.FloatField(null=False,blank=False,default=0)
    avg_buy_price = models.FloatField(null=False,blank=False,default=0)
    

