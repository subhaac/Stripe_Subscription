from django.db import models

class User_Account(models.Model):
    username = models.CharField(max_length=100)

class Payment_Method(models.Model):
        user = models.ForeignKey(to=User_Account, on_delete=models.CASCADE)
        card_type = models.CharField(max_length=50) # TODO: Give choice
        card_number =  models.BigIntegerField() 
        card_exp_month_year =  models.DateField(auto_now=False, auto_now_add=False)
        card_cvc =  models.IntegerField()
        
    
        
        
