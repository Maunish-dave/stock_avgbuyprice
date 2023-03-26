from django.db import models

class StockActions(models.Model):
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
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateTimeField(auto_now_add=True)
    ratio = models.FloatField(null=False,blank=False)

